#!/bin/bash
set -e
cd "$(dirname "$0")"
PROJECT_DIR="$PWD"
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
if [ -x "$PROJECT_DIR/backend/.venv/bin/python" ]; then
  PYTHON_BIN="$PROJECT_DIR/backend/.venv/bin/python"
elif [ -x "$HOME/Downloads/NutriTrack/backend/.venv/bin/python" ]; then
  PYTHON_BIN="$HOME/Downloads/NutriTrack/backend/.venv/bin/python"
else
  python3 -m venv "$PROJECT_DIR/backend/.venv"
  PYTHON_BIN="$PROJECT_DIR/backend/.venv/bin/python"
  "$PYTHON_BIN" -m pip install -r "$PROJECT_DIR/backend/requirements.txt"
fi
if [ ! -d "$PROJECT_DIR/frontend/node_modules" ]; then
  (cd "$PROJECT_DIR/frontend" && npm ci)
fi
"$PYTHON_BIN" - <<'PY'
import socket
for port in (8000, 5173):
    with socket.socket() as sock:
        if sock.connect_ex(('127.0.0.1', port)) == 0:
            print(f'A porta {port} já está em uso. Feche o servidor anterior antes de abrir outra cópia.')
            raise SystemExit(1)
PY
(cd "$PROJECT_DIR/backend" && exec "$PYTHON_BIN" -m uvicorn app.main:app --host 127.0.0.1 --port 8000) &
BACKEND_PID=$!
(cd "$PROJECT_DIR/frontend" && exec npm run dev -- --host 127.0.0.1 --port 5173 --strictPort) &
FRONTEND_PID=$!
trap 'kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true' EXIT INT TERM
printf '\nNutriTrack AC2: abra http://127.0.0.1:5173 no navegador.\nMantenha esta janela aberta. Para encerrar, pressione Control+C.\n\n'
wait
