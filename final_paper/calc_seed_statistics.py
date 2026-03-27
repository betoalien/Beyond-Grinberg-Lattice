from __future__ import annotations

from pathlib import Path

import numpy as np

from lattice_core import LatticeConfig, classify, ensure_dir, run_sim, summarize, write_csv, write_json


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "seed_statistics")
SEEDS = list(range(1, 31))


def mean_sd_ci(values):
    arr = np.asarray(values, dtype=float)
    mean = float(arr.mean())
    sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    ci95 = float(1.96 * sd / np.sqrt(len(arr))) if len(arr) > 1 else 0.0
    return mean, sd, ci95


def main() -> None:
    cases = {
        "coherent_switch": LatticeConfig(pulse_fraction=1.0),
        "fragmented_switch": LatticeConfig(J=0.20, noise=0.09, pulse_amp=-1.80, pulse_end=1700, pulse_fraction=0.45),
    }

    raw_rows = []
    summary_rows = []

    for case_name, base_cfg in cases.items():
        per_seed = []
        for seed in SEEDS:
            cfg = LatticeConfig(**{**base_cfg.__dict__, "seed": seed})
            summary = summarize(run_sim(cfg))
            summary["phase"] = classify(summary)
            summary["case"] = case_name
            raw_rows.append(summary)
            per_seed.append(summary)

        for key in [
            "transition_fragmentation",
            "transition_matched_error",
            "transition_lag_error",
            "post_matched_error",
            "mismatch_count",
        ]:
            mean, sd, ci95 = mean_sd_ci([row[key] for row in per_seed])
            summary_rows.append(
                {
                    "case": case_name,
                    "metric": key,
                    "n_seeds": len(per_seed),
                    "mean": mean,
                    "sd": sd,
                    "ci95_half_width": ci95,
                }
            )

    write_csv(OUT_DIR / "seed_statistics_raw.csv", raw_rows)
    write_csv(OUT_DIR / "seed_statistics_summary.csv", summary_rows)
    write_json(OUT_DIR / "seed_statistics_summary.json", {"rows": summary_rows})

    print("seed_statistics_summary")
    for row in summary_rows:
        if row["metric"] in {"transition_fragmentation", "transition_matched_error", "transition_lag_error"}:
            print(row)
    print(f"wrote: {OUT_DIR / 'seed_statistics_raw.csv'}")
    print(f"wrote: {OUT_DIR / 'seed_statistics_summary.csv'}")


if __name__ == "__main__":
    main()
