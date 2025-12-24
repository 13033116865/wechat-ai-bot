#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f "app.py" ]]; then
  echo "请在项目根目录执行（包含 app.py 的目录）。"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install -U pip
python -m pip install -r requirements.txt

if [[ ! -f ".env" && -f ".env.example" ]]; then
  cp .env.example .env
fi

python app.py

