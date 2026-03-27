#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PACKAGE_DIR"

echo "[1/6] Running baseline single-case reproduction"
python3 calc_single_case.py

echo "[2/6] Running coarse phase-grid reproduction"
python3 calc_phase_grid.py

echo "[3/6] Running alias-decoder evaluation"
python3 calc_alias_decoder.py

echo "[4/6] Running boundary-size sweep"
python3 calc_boundary_size_sweep.py

echo "[5/6] Running multi-seed statistics"
python3 calc_seed_statistics.py

echo "[6/6] Generating reproducible validation figure"
python3 plot_lattice_validation.py

echo "Done. Outputs are available under repro_outputs/"
