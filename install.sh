#!/bin/bash
echo "📦 UltraNOC Installer"

# Backend Setup
cd backend || exit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload &
cd ..

# Frontend Setup
cd frontend || exit
npm install
npm run dev &
cd ..

# Database Initialization
echo "💾 Initializing database..."
psql -U root -f init.sql

echo "✅ Installation complete. Visit http://localhost:3000"
