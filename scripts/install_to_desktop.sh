#!/usr/bin/env bash
set -euo pipefail

project_root() {
  local here
  here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  (cd "$here/.." && pwd)
}

detect_desktop_dir() {
  # Prefer XDG user-dirs config when available
  local cfg="$HOME/.config/user-dirs.dirs"
  if [[ -f "$cfg" ]]; then
    # shellcheck disable=SC1090
    source "$cfg" || true
    if [[ -n "${XDG_DESKTOP_DIR:-}" ]]; then
      # XDG_DESKTOP_DIR may contain $HOME
      eval echo "$XDG_DESKTOP_DIR"
      return 0
    fi
  fi

  if [[ -d "$HOME/Desktop" ]]; then
    echo "$HOME/Desktop"
    return 0
  fi
  if [[ -d "$HOME/桌面" ]]; then
    echo "$HOME/桌面"
    return 0
  fi

  # Fallback: create Desktop
  mkdir -p "$HOME/Desktop"
  echo "$HOME/Desktop"
}

SRC="$(project_root)"
DESKTOP_DIR="$(detect_desktop_dir)"
DEST="$DESKTOP_DIR/WeChatAssistant"

echo "源目录：$SRC"
echo "桌面目录：$DESKTOP_DIR"
echo "目标目录：$DEST"

rm -rf "$DEST"
mkdir -p "$DEST"

# Copy project without heavy/irrelevant artifacts
tar -C "$SRC" \
  --exclude "./.git" \
  --exclude "./venv" \
  --exclude "./.venv" \
  --exclude "./__pycache__" \
  --exclude "./.pytest_cache" \
  --exclude "./.mypy_cache" \
  --exclude "./.ruff_cache" \
  -cf - . | tar -C "$DEST" -xf -

echo
echo "已复制到桌面：$DEST"
echo "下一步："
echo "  cd \"$DEST\""
echo "  cp .env.example .env"
echo "  python -m venv .venv"
echo "  source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python app.py"

