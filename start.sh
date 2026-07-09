#!/bin/bash

# Funcție pentru a opri toate procesele pornite în fundal când apeși CTRL+C
cleanup() {
    echo -e "\n🛑 Se opresc serverele AeroActive..."
    # Oprim procesele folosind PID-urile salvate (Process ID)
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT

echo "Inițializare sistem AeroActive..."

echo "Se pornește Backend-ul pe portul 5001..."
uv run python app.py &
BACKEND_PID=$!

echo "Se încarcă modelul de Machine Learning..."

wait