from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


def sign(x: float) -> int:
    return 1 if x >= 0 else -1


@dataclass(frozen=True)
class LatticeConfig:
    N: int = 64
    observed: int = 16
    dt: float = 0.05
    steps: int = 3200
    delay_steps: int = 40
    alpha: float = 1.0
    beta: float = 1.0
    J: float = 0.45
    noise: float = 0.06
    pulse_start: int = 1400
    pulse_end: int = 1540
    pulse_amp: float = -1.45
    pulse_fraction: float = 1.0
    lag_steps: int = 120
    init_sector: int = 1
    seed: int = 7
    decoder_lambda: float = 0.35

    @property
    def x_star(self) -> float:
        return math.sqrt(self.alpha / self.beta)


@dataclass
class SimulationResult:
    config: LatticeConfig
    rows: List[Dict[str, float]]
    switch_step: int | None


TRANSITION_WINDOWS = {
    "pre": (-250, -20),
    "transition": (-20, 160),
    "post": (180, 430),
}


def run_sim(config: LatticeConfig) -> SimulationResult:
    rng = np.random.default_rng(config.seed)
    x = config.init_sector * config.x_star + rng.normal(0.0, 0.02, size=config.N)
    history = [x.copy() for _ in range(config.delay_steps + 1)]

    rows: List[Dict[str, float]] = []
    prev_sector = sign(float(x.mean()))
    switch_step = None
    active_sites = max(1, int(config.N * config.pulse_fraction))

    for t in range(config.steps):
        delayed = history[0]
        new_x = np.empty_like(x)
        for i in range(config.N):
            left = delayed[(i - 1) % config.N]
            right = delayed[(i + 1) % config.N]
            lap = left + right - 2.0 * x[i]
            drive = (
                config.pulse_amp
                if config.pulse_start <= t <= config.pulse_end and i < active_sites
                else 0.0
            )
            dx = (
                config.alpha * x[i]
                - config.beta * (x[i] ** 3)
                + config.J * lap
                + drive
            )
            dx += config.noise * math.sqrt(config.dt) * rng.normal(0.0, 1.0)
            new_x[i] = x[i] + config.dt * dx

        x = new_x
        history.append(x.copy())
        history.pop(0)

        m = float(x.mean())
        b = float(x[: config.observed].mean())
        sector = sign(m)
        coherence = abs(float(np.sign(x).mean()))
        fragmentation = 1.0 - coherence

        lam = config.decoder_lambda
        x_star = config.x_star
        matched_decoder = sector * x_star + lam * (b - sector * x_star)
        wrong_decoder = -sector * x_star + lam * (b + sector * x_star)

        lag_idx = max(0, t - config.lag_steps)
        lag_sector = rows[lag_idx]["sector"] if rows else sector
        lag_decoder = lag_sector * x_star + lam * (b - lag_sector * x_star)

        if switch_step is None and sector != prev_sector:
            switch_step = t
        prev_sector = sector

        rows.append(
            {
                "t": t,
                "m": m,
                "b": b,
                "sector": sector,
                "coherence": coherence,
                "fragmentation": fragmentation,
                "matched_decoder": matched_decoder,
                "wrong_decoder": wrong_decoder,
                "lag_decoder": lag_decoder,
                "matched_error": abs(matched_decoder - m),
                "wrong_error": abs(wrong_decoder - m),
                "lag_error": abs(lag_decoder - m),
            }
        )

    return SimulationResult(config=config, rows=rows, switch_step=switch_step)


def _window_slice(rows: Sequence[Dict[str, float]], switch_step: int, start: int, stop: int):
    lo = max(0, switch_step + start)
    hi = min(len(rows), switch_step + stop)
    return rows[lo:hi]


def summarize(result: SimulationResult) -> Dict[str, float]:
    if result.switch_step is None:
        raise RuntimeError("No sector switch observed for this configuration.")

    rows = result.rows
    sw = result.switch_step

    summary: Dict[str, float] = {
        "switch_step": sw,
        "x_star": result.config.x_star,
        "N": result.config.N,
        "observed": result.config.observed,
        "J": result.config.J,
        "noise": result.config.noise,
        "pulse_fraction": result.config.pulse_fraction,
        "lag_steps": result.config.lag_steps,
        "seed": result.config.seed,
    }

    for window_name, (start, stop) in TRANSITION_WINDOWS.items():
        block = _window_slice(rows, sw, start, stop)
        if not block:
            raise RuntimeError(f"Window {window_name} is empty.")
        for key in [
            "m",
            "b",
            "coherence",
            "fragmentation",
            "matched_error",
            "lag_error",
            "wrong_error",
        ]:
            summary[f"{window_name}_{key}"] = float(np.mean([r[key] for r in block]))

    mismatch_steps = []
    for idx, row in enumerate(rows):
        lag_idx = max(0, idx - result.config.lag_steps)
        lag_sector = rows[lag_idx]["sector"]
        if lag_sector != row["sector"]:
            mismatch_steps.append(idx)

    summary["mismatch_count"] = len(mismatch_steps)
    summary["mismatch_start"] = mismatch_steps[0] if mismatch_steps else None
    summary["mismatch_end"] = mismatch_steps[-1] if mismatch_steps else None
    summary["pre_sector"] = _window_slice(rows, sw, *TRANSITION_WINDOWS["pre"])[-1]["sector"]
    summary["post_sector"] = _window_slice(rows, sw, *TRANSITION_WINDOWS["post"])[0]["sector"]
    return summary


def classify(summary: Dict[str, float]) -> str:
    frag = summary["transition_fragmentation"]
    post = summary["post_matched_error"]
    lag = summary["transition_lag_error"]
    match = summary["transition_matched_error"]
    if frag > 0.2:
        return "fragmented_switch"
    if lag > 4 * max(match, 1e-9) and post < 0.05:
        return "coherent_switch_with_decoder_lag"
    if post < 0.05:
        return "coherent_switch"
    return "degraded_or_unrecoverable"


def alias_observation(boundary_value: float) -> float:
    return abs(boundary_value)


def fit_affine(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    xs_arr = np.asarray(xs, dtype=float)
    ys_arr = np.asarray(ys, dtype=float)
    mx = float(xs_arr.mean())
    my = float(ys_arr.mean())
    varx = float(np.sum((xs_arr - mx) ** 2))
    if varx == 0.0:
        return 0.0, my
    a = float(np.sum((xs_arr - mx) * (ys_arr - my)) / varx)
    c = my - a * mx
    return a, c


def collect_training(init_sector: int, observed: int, seeds: Iterable[int]) -> Tuple[List[float], List[float]]:
    xs: List[float] = []
    ys: List[float] = []
    for seed in seeds:
        cfg = LatticeConfig(
            observed=observed,
            steps=1200,
            pulse_amp=0.0,
            pulse_start=999999,
            pulse_end=1000000,
            init_sector=init_sector,
            seed=seed,
        )
        run = run_sim(cfg)
        for row in run.rows[200::25]:
            xs.append(alias_observation(row["b"]))
            ys.append(row["m"])
    return xs, ys


def evaluate_alias_decoder(config: LatticeConfig, training_observed: int | None = None) -> Dict[str, float]:
    observed = config.observed if training_observed is None else training_observed
    pos_x, pos_y = collect_training(1, observed, [1, 3, 5, 7, 9])
    neg_x, neg_y = collect_training(-1, observed, [2, 4, 6, 8, 10])
    a_pos, c_pos = fit_affine(pos_x, pos_y)
    a_neg, c_neg = fit_affine(neg_x, neg_y)
    a_glob, c_glob = fit_affine(pos_x + neg_x, pos_y + neg_y)

    run = run_sim(config)
    summary = summarize(run)
    sw = summary["switch_step"]

    blocks = {name: [] for name in TRANSITION_WINDOWS}
    for idx, row in enumerate(run.rows):
        z = alias_observation(row["b"])
        m = row["m"]
        sector = row["sector"]
        lag_sector = run.rows[max(0, idx - config.lag_steps)]["sector"]

        if sector >= 0:
            m_match = a_pos * z + c_pos
            m_wrong = a_neg * z + c_neg
        else:
            m_match = a_neg * z + c_neg
            m_wrong = a_pos * z + c_pos

        m_lag = (a_pos * z + c_pos) if lag_sector >= 0 else (a_neg * z + c_neg)
        m_global = a_glob * z + c_glob
        vals = (
            abs(m_match - m),
            abs(m_lag - m),
            abs(m_wrong - m),
            abs(m_global - m),
        )

        for window_name, (start, stop) in TRANSITION_WINDOWS.items():
            if sw + start <= idx < sw + stop:
                blocks[window_name].append(vals)

    out = {
        "observed": observed,
        "a_pos": a_pos,
        "c_pos": c_pos,
        "a_neg": a_neg,
        "c_neg": c_neg,
        "a_global": a_glob,
        "c_global": c_glob,
        "switch_step": sw,
    }
    labels = ["matched", "lagged", "wrong", "global"]
    for window_name, block in blocks.items():
        arr = np.asarray(block, dtype=float)
        for j, label in enumerate(labels):
            out[f"{window_name}_{label}"] = float(arr[:, j].mean())
    return out


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_csv(path: str | Path, rows: Sequence[Dict[str, object]]) -> None:
    path = Path(path)
    ensure_dir(path.parent)
    if not rows:
        raise ValueError("No rows to write.")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: str | Path, data: Dict[str, object]) -> None:
    import json

    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def config_dict(config: LatticeConfig) -> Dict[str, object]:
    d = asdict(config)
    d["x_star"] = config.x_star
    return d
