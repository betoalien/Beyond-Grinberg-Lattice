# Supplementary Methods: Computational Reproducibility for `Beyond the Grinberg Lattice`

## Scope
This supplement documents the exact computational conventions used in the companion reproducibility package distributed with the manuscript. Its purpose is to reduce ambiguity for independent inspection, notebook translation, or reimplementation.

These methods support only the restricted claim made in the manuscript:

> A delayed lattice model can reproducibly separate coherent sector switching, fragmented transitions, and decoder-lag penalties under partial observation.

They do **not** validate Grinberg's ontology, literal holographic-brain implementation, or paranormal interpretations.

## Software environment
### Tested interpreter
- Python `3.12.10`

### Tested package versions
- `numpy==2.4.2`
- `pandas==3.0.0`
- `matplotlib==3.10.8`

Environment files included in this package:
- `requirements.txt`
- `environment.yml`

## File layout
Core reproducibility files:
- `lattice_core.py`
- `calc_single_case.py`
- `calc_phase_grid.py`
- `calc_alias_decoder.py`
- `calc_boundary_size_sweep.py`
- `calc_seed_statistics.py`
- `plot_lattice_validation.py`

Generated outputs:
- `repro_outputs/single_case/`
- `repro_outputs/phase_grid/`
- `repro_outputs/alias_decoder/`
- `repro_outputs/boundary_size_sweep/`
- `repro_outputs/seed_statistics/`
- `repro_outputs/figures/`

## Core dynamical system
The delayed lattice uses a one-dimensional periodic chain of length $N$ with state $x_i(t)$ updated in discrete Euler steps of size $dt$ according to the manuscript equation

$$
\frac{d x_i}{dt} = \alpha x_i - \beta x_i^3 + J\big(x_{i-1}(t-\tau_d) + x_{i+1}(t-\tau_d) - 2x_i(t)\big) + u_i(t) + \sigma \eta_i(t).
$$

In code, delay is implemented through a fixed-length history buffer of `delay_steps + 1` states. Noise is sampled from a Gaussian distribution with a deterministic random seed via `numpy.random.default_rng(seed)`.

## Default baseline configuration
The baseline configuration in `LatticeConfig()` is:

- `N = 64`
- `observed = 16`
- `dt = 0.05`
- `steps = 3200`
- `delay_steps = 40`
- `alpha = 1.0`
- `beta = 1.0`
- `J = 0.45`
- `noise = 0.06`
- `pulse_start = 1400`
- `pulse_end = 1540`
- `pulse_amp = -1.45`
- `pulse_fraction = 1.0`
- `lag_steps = 120`
- `init_sector = 1`
- `seed = 7`
- `decoder_lambda = 0.35`

The characteristic local magnitude is computed as

$$
x_* = \sqrt{\alpha/\beta}.
$$

## Forcing geometry
The forcing term is applied only to the first

$$
\max(1, \lfloor N \cdot \text{pulse\_fraction} \rfloor)
$$

sites during the interval

$$
pulse\_start \le t \le pulse\_end.
$$

This is operationally important because pulse geometry is one of the main controls separating coherent and fragmented transitions.

## Observables and metrics
### Bulk order parameter

$$
m(t)=\frac{1}{N}\sum_{i=1}^N x_i(t)
$$

### Boundary observable

$$
b(t)=\frac{1}{|A|}\sum_{i\in A}x_i(t)
$$

where `A` is the observed prefix of size `observed`.

### Sector label

$$
s(t)=\operatorname{sign}(m(t))\in\{+1,-1\}
$$

with the convention `sign(0)=+1` in code.

### Coherence and fragmentation

$$
C(t)=\left|\frac{1}{N}\sum_{i=1}^N\operatorname{sign}(x_i(t))\right|,
\qquad
F(t)=1-C(t).
$$

### Sector-conditioned decoder

$$
D_s(b)=s x_* + \lambda(b-sx_*), \qquad \lambda=0.35.
$$

Three decoder outputs are tracked:
- matched decoder,
- wrong decoder,
- lagged decoder.

Errors are absolute differences from the latent order parameter $m(t)$.

## Time windows used in summaries
All single-case summaries are computed relative to the first detected sector switch `switch_step`.

The windows are:
- `pre`: `[switch_step - 250, switch_step - 20)`
- `transition`: `[switch_step - 20, switch_step + 160)`
- `post`: `[switch_step + 180, switch_step + 430)`

These windows are hard-coded in `lattice_core.py` as:

```python
TRANSITION_WINDOWS = {
    "pre": (-250, -20),
    "transition": (-20, 160),
    "post": (180, 430),
}
```

## Sector switch detection
`switch_step` is defined as the first time index at which the sign of `m(t)` differs from the previous step. If no switch is observed, the code raises a `RuntimeError` in summary mode.

## Mismatch interval and decoder lag
The lagged decoder uses the sector label from

$$
t-\Delta
$$

where `Δ = lag_steps` in discrete time. The mismatch interval counts the number of steps for which the delayed sector label differs from the current sector label.

This is reported through:
- `mismatch_count`
- `mismatch_start`
- `mismatch_end`

## Classification rule for phase-grid experiments
The coarse phase grid uses the following decision rule on summary statistics:

1. If `transition_fragmentation > 0.2` -> `fragmented_switch`
2. Else if `transition_lag_error > 4 * transition_matched_error` and `post_matched_error < 0.05` -> `coherent_switch_with_decoder_lag`
3. Else if `post_matched_error < 0.05` -> `coherent_switch`
4. Else -> `degraded_or_unrecoverable`

This rule is heuristic. It is a reporting classifier, not a theorem.

## Alias-decoder protocol
To test whether sector labels are genuinely necessary, the boundary observation is sign-aliased:

$$
z(t)=|b(t)|.
$$

Training data are collected separately from positive-sector and negative-sector stationary runs using seeds:
- positive sector: `[1, 3, 5, 7, 9]`
- negative sector: `[2, 4, 6, 8, 10]`

For each sector family, an affine decoder

$$
\hat m = a z + c
$$

is fit by ordinary least squares using the helper `fit_affine`.

At evaluation time, four reconstruction modes are compared:
- matched sector-conditioned decoder,
- lagged sector-conditioned decoder,
- wrong-sector decoder,
- global decoder fit to pooled data.

## Boundary-size sweep
The boundary-size sweep evaluates the coherent-switch case at:
- `observed = 4, 8, 16, 24, 32`

The reported outputs are:
- `transition_matched`
- `transition_lagged`
- `transition_wrong`
- `transition_global`
- `post_matched`
- `post_lagged`

The intended use is to test whether larger observed boundaries rescue stale decoding. In the current model they improve matched reconstruction but do not eliminate lag penalty.

## Multi-seed statistics
`calc_seed_statistics.py` uses seeds:

$$
\{1,2,\dots,30\}
$$

for two anchor conditions:
- coherent-switch condition: `pulse_fraction = 1.0`
- fragmented-switch condition: `J = 0.20`, `noise = 0.09`, `pulse_amp = -1.80`, `pulse_end = 1700`, `pulse_fraction = 0.45`

For each metric, the script reports:
- mean,
- sample standard deviation (`ddof=1`),
- approximate 95% confidence half-width

computed as

$$
1.96\cdot \frac{s}{\sqrt{n}}.
$$

This is a normal-approximation interval, included as a descriptive robustness summary rather than a formal inferential claim.

## Output formats
Machine-readable outputs are written as:
- CSV for row-wise inspection,
- JSON for structured summaries,
- PNG for figures.

This is intentional so the same results can be inspected in plain text, imported into notebooks, or re-plotted without rerunning every script.

## Recommended execution order
From the project root:

```bash
python3 final_paper/calc_single_case.py
python3 final_paper/calc_phase_grid.py
python3 final_paper/calc_alias_decoder.py
python3 final_paper/calc_boundary_size_sweep.py
python3 final_paper/calc_seed_statistics.py
python3 final_paper/plot_lattice_validation.py
```

## Known limitations of the computational package
1. The model is still a toy model.
2. The reporting classifier is heuristic.
3. The confidence intervals are descriptive rather than model-based.
4. The alias-decoder fit is affine and intentionally simple.
5. The package demonstrates internal reproducibility, not biological confirmation.
