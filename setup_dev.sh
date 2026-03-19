#!/usr/bin/env bash
"""
Development setup script for PhantomGuard 2.0
"""

echo "🚀 Setting up PhantomGuard 2.0 Development Environment"
echo "======================================================"

# Backend setup
echo "📦 Setting up Backend..."
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "from app.database.init_db import create_tables; create_tables()"
echo "✅ Backend setup complete"

# Frontend setup
echo "🎨 Setting up Frontend..."
cd ../frontend
npm install
echo "✅ Frontend setup complete"

# Agent setup
echo "🤖 Setting up Agent..."
cd ../agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
echo "✅ Agent setup complete"

echo ""
echo "🎉 Setup complete! You can now run:"
echo "  Backend:  python run_backend.py"
echo "  Frontend: ./run_frontend.sh (or run_frontend.bat on Windows)"
echo "  Agent:    python run_agent.py"
echo ""
echo "📊 API Documentation will be available at: http://localhost:8000/docs"
echo "🎨 Frontend will be available at: http://localhost:3000"