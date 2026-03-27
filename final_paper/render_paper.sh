#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PACKAGE_DIR"

TITLE='Beyond the Grinberg Lattice: Boundary Precision, Sector Switching, and Decoder Lag in a Holographic-QEC-Inspired Model of Coherence and Recoverability'
AUTHOR='Alberto Cardenas'
DATE='2026-03-26'

TMP_MD="/tmp/beyond-grinberg-lattice-render.md"
TMP_HTML="/tmp/beyond-grinberg-lattice-render.embedded.html"

awk 'BEGIN{flag=0} /^## Abstract/{flag=1} flag{print}' beyond-grinberg-lattice.md > "$TMP_MD"

pandoc "$TMP_MD" \
  --standalone \
  --embed-resources \
  --from markdown+tex_math_dollars \
  --to html5 \
  --css /tmp/grinberg-paper.css \
  --mathjax='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js' \
  -M title="$TITLE" \
  -M author="$AUTHOR" \
  -M date="$DATE" \
  --resource-path=".:$PACKAGE_DIR:$PACKAGE_DIR/figures:$PACKAGE_DIR/repro_outputs:experiments" \
  -o "$TMP_HTML"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=12000 \
  --print-to-pdf="$PACKAGE_DIR/beyond-grinberg-lattice.pdf" \
  --no-pdf-header-footer \
  "file://$TMP_HTML"

pandoc "$TMP_MD" \
  --standalone \
  --from markdown+tex_math_dollars \
  --to latex \
  -M title="$TITLE" \
  -M author="$AUTHOR" \
  -M date="$DATE" \
  --include-in-header=/tmp/grinberg-paper-header.tex \
  --resource-path=".:$PACKAGE_DIR:$PACKAGE_DIR/figures:$PACKAGE_DIR/repro_outputs:experiments" \
  -o "$PACKAGE_DIR/beyond-grinberg-lattice.tex"

echo "Rendered: $PACKAGE_DIR/beyond-grinberg-lattice.pdf"
echo "Rendered: $PACKAGE_DIR/beyond-grinberg-lattice.tex"
