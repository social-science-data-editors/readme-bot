#!/usr/bin/env bash
# Create (or reuse) the website's Python environment and install Jupyter Book.
# Idempotent: safe to re-run; pip skips packages that are already installed.
# Then:  cd docs && .venv/bin/jupyter-book start      (live preview)
#        cd docs && .venv/bin/jupyter-book build --html   (static site in _build/html)
set -euo pipefail
cd "$(dirname "$0")"
VENV=${VENV:-.venv}
if [ ! -x "$VENV/bin/python" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet -r requirements.txt
echo "Environment ready: cd docs && $VENV/bin/jupyter-book start"
