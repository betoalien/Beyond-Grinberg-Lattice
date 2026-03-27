# Beyond the Grinberg Lattice

Repository for the manuscript and computational artifact:

**Beyond the Grinberg Lattice: Boundary Precision, Sector Switching, and Decoder Lag in a Holographic-QEC-Inspired Model of Coherence and Recoverability**

## Author
**Alberto Cardenas**  
Contact: **iam@albertocardenas.com**

## What this repository contains
This repository combines:
- the manuscript in PDF, LaTeX, and Markdown form,
- a reproducibility package for the delayed-lattice toy model,
- machine-readable outputs used in the paper,
- a notebook scaffold for inspection and extension,
- a `docs/` folder prepared for GitHub Pages using Just the Docs,
- environment files, citation metadata, and licensing.

## Central claim boundary
This repository supports a narrow computational claim:

> A delayed lattice model can reproducibly distinguish coherent sector switching, fragmented transitions, and decoder-lag penalties under partial observation.

It does **not** establish literal holographic-brain implementation, confirm Grinberg's original ontology, or validate extraordinary/paranormal interpretations.

## Repository layout
```text
beyond-grinberg-lattice/
  README.md
  .gitignore
  CITATION.cff
  LICENSE
  final_paper/
    beyond-grinberg-lattice.pdf
    beyond-grinberg-lattice.tex
    beyond-grinberg-lattice.md
    README_reproducibility.md
    SUPPLEMENTARY_METHODS.md
    requirements.txt
    environment.yml
    run_all_repro.sh
    lattice_core.py
    calc_*.py
    plot_lattice_validation.py
    beyond-grinberg-lattice-reproducibility.ipynb
    repro_outputs/
  docs/
    _config.yml
    index.md
    paper.md
    reproducibility.md
    links.md
    assets/downloads/beyond-grinberg-lattice.pdf
```

## Primary files
- `final_paper/beyond-grinberg-lattice.pdf` — main paper for reading/sharing
- `final_paper/beyond-grinberg-lattice.tex` — LaTeX source
- `final_paper/beyond-grinberg-lattice.md` — canonical Markdown manuscript source
- `final_paper/README_reproducibility.md` — reproduction overview
- `final_paper/SUPPLEMENTARY_METHODS.md` — exact computational conventions
- `final_paper/CITATION.cff` — artifact citation metadata
- `final_paper/render_paper.sh` — regenerates the PDF and LaTeX bundle with embedded figure assets

## Quick start
### Option A: Conda / mamba
```bash
conda env create -f final_paper/environment.yml
conda activate beyond-grinberg-lattice
bash final_paper/run_all_repro.sh
```

### Option B: pip
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r final_paper/requirements.txt
bash final_paper/run_all_repro.sh
```

## Expected generated outputs
The one-command runner regenerates machine-readable outputs under:
- `final_paper/repro_outputs/single_case/`
- `final_paper/repro_outputs/phase_grid/`
- `final_paper/repro_outputs/alias_decoder/`
- `final_paper/repro_outputs/boundary_size_sweep/`
- `final_paper/repro_outputs/seed_statistics/`
- `final_paper/repro_outputs/figures/`

## Citation
If you use the manuscript or computational artifact, see:
- root `CITATION.cff`
- `final_paper/CITATION.cff`

## Provenance note
The manuscript and computational artifact were developed under the direction and final editorial control of Alberto Cardenas. Feynman, an AI-based research assistant, was used during literature triage, code drafting, artifact organization, and iterative manuscript refinement. Final scientific framing, claim boundaries, interpretive choices, and release decisions were made by Alberto Cardenas.

## GitHub Pages
A `docs/` folder is already prepared for **GitHub Pages** using **Just the Docs**.

After pushing to GitHub, enable Pages from:
- **Settings -> Pages**
- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/docs`

## Ready to publish
At this point the repository root can be committed and pushed to GitHub as-is.
