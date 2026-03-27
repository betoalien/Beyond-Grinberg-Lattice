# Reproducibility package for `beyond-grinberg-lattice`

This folder now includes a minimal, paper-aligned Python package for reproducing the main lattice calculations **without** the non-scientific language that appeared in the earlier illustrative script.

## Why this was added
An earlier illustrative figure used during drafting was not a suitable validation artifact for other researchers because:
- it used non-technical labels such as `faith`, `miracles`, and `anomalies`,
- it implemented an ad hoc scalar fidelity process rather than the delayed bistable lattice used in the paper,
- it did not expose the actual quantities claimed in the manuscript,
- and it did not separate simulation, summary metrics, and plotting into reproducible components.

The replacement scripts below fix that.

## Files
- `lattice_core.py` — core delayed-lattice model, summary metrics, phase classifier, and alias-decoder calculations.
- `calc_single_case.py` — exports a full baseline time series and summary metrics.
- `calc_phase_grid.py` — reproduces the coarse phase grid over coupling and pulse geometry.
- `calc_alias_decoder.py` — tests when sector-conditioned decoding is required under sign-aliased observations.
- `calc_boundary_size_sweep.py` — measures how decoder performance changes as the observed boundary size increases.
- `calc_seed_statistics.py` — computes multi-seed summary statistics, standard deviations, and approximate 95% confidence intervals.
- `plot_lattice_validation.py` — generates a paper-aligned validation figure.

## Outputs
Running the scripts creates machine-readable artifacts in:
- `repro_outputs/single_case/`
- `repro_outputs/phase_grid/`
- `repro_outputs/alias_decoder/`
- `repro_outputs/boundary_size_sweep/`
- `repro_outputs/seed_statistics/`
- `repro_outputs/figures/`

These outputs are intentionally separated so they can be moved into Jupyter notebooks later.

## Environment
Tested with:
- Python `3.12.10`
- `numpy==2.4.2`
- `pandas==3.0.0`
- `matplotlib==3.10.8`

Environment files included here:
- `requirements.txt`
- `environment.yml`

Project metadata files included here:
- `CITATION.cff`
- `LICENSE`
- `run_all_repro.sh`

## Recommended execution order
From the project root:

```bash
bash run_all_repro.sh
```

Equivalent step-by-step commands:

```bash
python3 calc_single_case.py
python3 calc_phase_grid.py
python3 calc_alias_decoder.py
python3 calc_boundary_size_sweep.py
python3 calc_seed_statistics.py
python3 plot_lattice_validation.py
```

## Minimal validation claims supported by these scripts
1. A coherent sector switch can occur with very low fragmentation.
2. A lagged decoder incurs a larger transition penalty than the matched decoder.
3. Partial forcing drives fragmented transitions more often than global forcing.
4. Under sign-aliased boundary observations, sector-conditioned decoding outperforms lagged, wrong, and global decoders.
5. Increasing the observed boundary size improves matched reconstruction but does not rescue a stale decoder.
6. The above claims can be summarized over repeated random seeds rather than a single cherry-picked run.

## Supplementary methods
A more explicit methods companion is now included at:
- `SUPPLEMENTARY_METHODS.md`

It documents:
- exact parameter defaults,
- time-window definitions,
- phase-classification thresholds,
- training/evaluation splits for the alias-decoder test,
- multi-seed summary conventions,
- and software-version details.

## Important claim boundaries
These scripts do **not** validate Grinberg's ontology, literal holographic brain claims, or paranormal interpretations.
They validate only the narrower claim used in the manuscript: that a delayed lattice model can separate coherent switching, fragmentation, and decoder-lag effects under partial observation.
