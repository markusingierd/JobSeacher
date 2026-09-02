#!/bin/bash
# ==============================================================================
# FinnJobScout UI – Stoppskript for macOS
# ==============================================================================
# Dobbelklikk på denne filen i Finder for å stoppe både backend og frontend!
# ==============================================================================

echo "=================================================="
echo "🛑 Stopper FinnJobScout UI..."
echo "=================================================="

# Finn og stopp prosesser på port 8000 (FastAPI) og port 3000 (Vite)
PID_8000=$(lsof -ti:8000)
PID_3000=$(lsof -ti:3000)

if [ -n "$PID_8000" ]; then
    echo "  -> Stopper Python FastAPI Backend (PID: $PID_8000)..."
    kill -9 $PID_8000 2>/dev/null
fi

if [ -n "$PID_3000" ]; then
    echo "  -> Stopper TypeScript React Frontend (PID: $PID_3000)..."
    kill -9 $PID_3000 2>/dev/null
fi

echo ""
echo "✅ Prosjektet er helt stoppet! Ingen prosesser kjører i bakgrunnen."
echo "=================================================="
sleep 1.5
