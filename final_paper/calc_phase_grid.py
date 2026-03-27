from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from lattice_core import LatticeConfig, classify, ensure_dir, run_sim, summarize, write_csv, write_json


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "phase_grid")
J_VALUES = [0.20, 0.30, 0.45, 0.60]
PULSE_FRAC_VALUES = [0.45, 0.60, 0.80, 1.00]
SEEDS = [7, 11, 19]


def main() -> None:
    rows = []
    majority = {}
    counts = defaultdict(Counter)

    for J in J_VALUES:
        for pulse_fraction in PULSE_FRAC_VALUES:
            for seed in SEEDS:
                cfg = LatticeConfig(J=J, pulse_fraction=pulse_fraction, seed=seed)
                try:
                    summary = summarize(run_sim(cfg))
                    phase = classify(summary)
                    row = {
                        "J": J,
                        "pulse_fraction": pulse_fraction,
                        "seed": seed,
                        "phase": phase,
                        "transition_fragmentation": summary["transition_fragmentation"],
                        "transition_matched_error": summary["transition_matched_error"],
                        "transition_lag_error": summary["transition_lag_error"],
                        "post_matched_error": summary["post_matched_error"],
                    }
                except RuntimeError:
                    row = {
                        "J": J,
                        "pulse_fraction": pulse_fraction,
                        "seed": seed,
                        "phase": "no_switch",
                        "transition_fragmentation": None,
                        "transition_matched_error": None,
                        "transition_lag_error": None,
                        "post_matched_error": None,
                    }
                rows.append(row)
                counts[(J, pulse_fraction)][row["phase"]] += 1

    for key, counter in counts.items():
        majority[key] = counter.most_common(1)[0][0]

    write_csv(OUT_DIR / "phase_grid_raw.csv", rows)
    write_json(
        OUT_DIR / "phase_grid_majority.json",
        {
            "grid": [
                {
                    "J": J,
                    "pulse_fraction": pulse_fraction,
                    "majority_phase": majority[(J, pulse_fraction)],
                    "counts": dict(counts[(J, pulse_fraction)]),
                }
                for J in J_VALUES
                for pulse_fraction in PULSE_FRAC_VALUES
            ]
        },
    )

    print("phase_grid_majority")
    for J in J_VALUES:
        labels = [majority[(J, pf)] for pf in PULSE_FRAC_VALUES]
        print(f"J={J}: {labels}")
    print(f"wrote: {OUT_DIR / 'phase_grid_raw.csv'}")
    print(f"wrote: {OUT_DIR / 'phase_grid_majority.json'}")


if __name__ == "__main__":
    main()
