from __future__ import annotations

from pathlib import Path

import numpy as np

from lattice_core import LatticeConfig, config_dict, ensure_dir, run_sim, summarize, write_csv, write_json


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "single_case")


def main() -> None:
    cfg = LatticeConfig()
    result = run_sim(cfg)
    summary = summarize(result)

    rows = []
    for row in result.rows:
        rows.append({k: (float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in row.items()})

    write_csv(OUT_DIR / "single_case_timeseries.csv", rows)
    write_json(
        OUT_DIR / "single_case_summary.json",
        {
            "config": config_dict(cfg),
            "summary": summary,
            "scientific_interpretation": {
                "matched_error": "decoder error when the sector label matches the current lattice sector",
                "lag_error": "decoder error when the decoder uses a delayed sector label",
                "wrong_error": "decoder error under the explicitly mismatched sector label",
                "fragmentation": "1 - coherence, used as a proxy for local disagreement during transition",
            },
        },
    )

    print("single_case_summary")
    for key in [
        "switch_step",
        "pre_sector",
        "post_sector",
        "transition_fragmentation",
        "transition_matched_error",
        "transition_lag_error",
        "post_matched_error",
        "mismatch_count",
    ]:
        print(f"{key}: {summary[key]}")
    print(f"wrote: {OUT_DIR / 'single_case_timeseries.csv'}")
    print(f"wrote: {OUT_DIR / 'single_case_summary.json'}")


if __name__ == "__main__":
    main()
