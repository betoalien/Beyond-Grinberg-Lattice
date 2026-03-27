---
layout: default
title: Reproducibility
nav_order: 3
---

# Reproducibility

## Package location
The computational artifact is stored in:
- `final_paper/`

## Main files
- `final_paper/lattice_core.py`
- `final_paper/calc_single_case.py`
- `final_paper/calc_phase_grid.py`
- `final_paper/calc_alias_decoder.py`
- `final_paper/calc_boundary_size_sweep.py`
- `final_paper/calc_seed_statistics.py`
- `final_paper/plot_lattice_validation.py`
- `final_paper/run_all_repro.sh`
- `final_paper/README_reproducibility.md`
- `final_paper/SUPPLEMENTARY_METHODS.md`

## Run everything
From the repository root:

```bash
bash final_paper/run_all_repro.sh
```

## Outputs
Running the package regenerates:
- single-case time series and summary metrics,
- coarse phase-grid outputs,
- alias-decoder metrics,
- boundary-size sweep outputs,
- multi-seed summary statistics,
- reproducible figure assets.

## Environment
You can use either:
- `final_paper/requirements.txt`
- `final_paper/environment.yml`

## Important boundary
The package is intended to support computational replication of the reported toy-model results. It is not, by itself, empirical confirmation of literal holographic-brain implementation or extraordinary ontological claims.
