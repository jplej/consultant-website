#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "→ Creating virtualenv with uv"
  uv venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "→ Installing Python deps"
uv pip install -q -r requirements.txt

if [ ! -d node_modules ]; then
  echo "→ Installing Node deps"
  npm install --silent
fi

cleanup() {
  echo
  echo "→ Shutting down"
  kill 0 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "→ Starting Tailwind (watch) + Flask (debug) — one terminal"
npx tailwindcss -i static/css/input.css -o static/css/site.css --watch=always &

export FLASK_APP=app.py
flask run --debug
