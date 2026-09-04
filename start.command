#!/bin/bash
# ==============================================================================
# FinnJobScout UI – Oppstartsskript for macOS
# ==============================================================================
# Dobbelklikk på denne filen i Finder for å starte både backend og frontend!
# ==============================================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=================================================="
echo "🚀 Starter FinnJobScout UI..."
echo "=================================================="

# Drepe eventuelle gamle prosesser på port 8000 og 3000 først
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Sjekk at virtual environment finnes
if [ ! -d ".venv" ]; then
    echo "📦 Oppretter Python venv..."
    python3 -m venv .venv
    .venv/bin/pip install -r backend/requirements.txt
fi

# Sjekk at node_modules finnes i frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installerer frontend npm-pakker..."
    cd frontend && npm install && cd ..
fi

echo "⚙️ Starter Python FastAPI Backend (port 8000)..."
.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "🎨 Starter TypeScript React Frontend (port 3000)..."
cd frontend
npm run dev -- --host 0.0.0.0 --port 3000 &
FRONTEND_PID=$!
cd "$DIR"

# Rydd opp prosesser kun dersom brukeren trykker Ctrl+C (SIGINT/SIGTERM)
cleanup() {
    echo ""
    echo "🛑 Stopper FinnJobScout..."
    kill -9 $BACKEND_PID $FRONTEND_PID 2>/dev/null
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo "✅ Alle servere stoppet!"
    exit 0
}

trap cleanup INT TERM

# Vent 3 sekunder slik at både FastAPI og Vite rekker å starte helt opp
sleep 3
echo "🌐 Åpner http://localhost:3000 i nettleseren..."
open "http://localhost:3000"

echo ""
echo "=================================================="
echo "✨ FinnJobScout UI Kjører!"
echo "   - Dashboard: http://localhost:3000"
echo "   - REST API:  http://localhost:8000"
echo ""
echo "💡 Slik stopper du appen:"
echo "   • Trykk Ctrl+C i dette terminalvinduet"
echo "   • ELLER dobbelklikk på stop.command i Finder!"
echo "=================================================="

wait
