from __future__ import annotations

from pathlib import Path

from lattice_core import LatticeConfig, ensure_dir, evaluate_alias_decoder, write_csv, write_json


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "alias_decoder")


def main() -> None:
    configs = [
        ("coherent_switch", LatticeConfig(observed=16, seed=101)),
        (
            "fragmented_switch",
            LatticeConfig(observed=16, J=0.20, noise=0.09, pulse_amp=-1.80, pulse_end=1700, pulse_fraction=0.45, seed=101),
        ),
    ]
    rows = []
    for case_name, cfg in configs:
        metrics = evaluate_alias_decoder(cfg)
        metrics["case"] = case_name
        rows.append(metrics)

    ordered = []
    keys = ["case", "observed", "switch_step"] + [
        k for k in rows[0].keys() if k not in {"case", "observed", "switch_step"}
    ]
    for row in rows:
        ordered.append({k: row[k] for k in keys if k in row})

    write_csv(OUT_DIR / "alias_decoder_metrics.csv", ordered)
    write_json(OUT_DIR / "alias_decoder_metrics.json", {"rows": ordered})

    print("alias_decoder_metrics")
    for row in ordered:
        print(
            row["case"],
            {
                "transition_matched": row["transition_matched"],
                "transition_lagged": row["transition_lagged"],
                "transition_wrong": row["transition_wrong"],
                "transition_global": row["transition_global"],
            },
        )
    print(f"wrote: {OUT_DIR / 'alias_decoder_metrics.csv'}")
    print(f"wrote: {OUT_DIR / 'alias_decoder_metrics.json'}")


if __name__ == "__main__":
    main()
