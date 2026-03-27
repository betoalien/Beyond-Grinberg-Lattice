from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from lattice_core import LatticeConfig, ensure_dir, run_sim, summarize


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = ensure_dir(BASE_DIR / "repro_outputs" / "figures")


def main() -> None:
    cfg = LatticeConfig(seed=7)
    result = run_sim(cfg)
    summary = summarize(result)
    rows = result.rows
    t = np.array([r["t"] for r in rows])
    m = np.array([r["m"] for r in rows])
    frag = np.array([r["fragmentation"] for r in rows])
    matched = np.array([r["matched_error"] for r in rows])
    lagged = np.array([r["lag_error"] for r in rows])

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

    axes[0].plot(t, m, color="#1f77b4", lw=2)
    axes[0].axhline(0.0, color="black", lw=0.8, alpha=0.5)
    axes[0].axvline(summary["switch_step"], color="#d62728", ls="--", lw=1.5, label="sector switch")
    axes[0].set_ylabel("order parameter m(t)")
    axes[0].legend(loc="best")
    axes[0].set_title("Reproducible lattice validation: coherent sector switch and decoder-lag penalty")

    axes[1].plot(t, frag, color="#ff7f0e", lw=2)
    axes[1].axvline(summary["switch_step"], color="#d62728", ls="--", lw=1.5)
    axes[1].set_ylabel("fragmentation F(t)")

    axes[2].plot(t, matched, color="#2ca02c", lw=2, label="matched decoder error")
    axes[2].plot(t, lagged, color="#9467bd", lw=2, label="lagged decoder error")
    axes[2].axvline(summary["switch_step"], color="#d62728", ls="--", lw=1.5)
    axes[2].set_ylabel("abs reconstruction error")
    axes[2].set_xlabel("time step")
    axes[2].legend(loc="best")

    for ax in axes:
        ax.grid(alpha=0.25)

    fig.tight_layout()
    png_path = OUT_DIR / "Figure_1_reproducible.png"
    fig.savefig(png_path, dpi=180)
    print(f"wrote: {png_path}")


if __name__ == "__main__":
    main()
