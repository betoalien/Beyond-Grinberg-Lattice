from __future__ import annotations

from pathlib import Path

from lattice_core import LatticeConfig, ensure_dir, evaluate_alias_decoder, write_csv, write_json


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "boundary_size_sweep")
OBSERVED_VALUES = [4, 8, 16, 24, 32]


def main() -> None:
    rows = []
    for observed in OBSERVED_VALUES:
        cfg = LatticeConfig(observed=observed, seed=101)
        metrics = evaluate_alias_decoder(cfg)
        rows.append(
            {
                "observed": observed,
                "transition_matched": metrics["transition_matched"],
                "transition_lagged": metrics["transition_lagged"],
                "transition_wrong": metrics["transition_wrong"],
                "transition_global": metrics["transition_global"],
                "post_matched": metrics["post_matched"],
                "post_lagged": metrics["post_lagged"],
            }
        )

    write_csv(OUT_DIR / "boundary_size_sweep.csv", rows)
    write_json(OUT_DIR / "boundary_size_sweep.json", {"rows": rows})

    print("boundary_size_sweep")
    for row in rows:
        print(row)
    print(f"wrote: {OUT_DIR / 'boundary_size_sweep.csv'}")
    print(f"wrote: {OUT_DIR / 'boundary_size_sweep.json'}")


if __name__ == "__main__":
    main()
