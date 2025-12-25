#!/bin/bash
# Development startup script for AuraStudio Omni - Linux/macOS

set -e

echo "🚀 AuraStudio Omni - Development Startup"
echo "=========================================="

# Check Python
echo "✓ Checking Python installation..."
python --version

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r api/requirements.txt --quiet

# Create .env if not exists
if [ ! -f ".env.development" ]; then
    echo "⚠ Creating .env.development (please configure with real keys)"
    cp .env.development.example .env.development 2>/dev/null || echo "Note: .env.development.example not found"
fi

# Run database migrations (if PostgreSQL is running)
echo ""
echo "📦 Database Setup (optional - requires PostgreSQL)"
echo "To set up database, run:"
echo "  cd db && psql -f migrations/001_initial_schema.sql -U postgres"
echo "  psql -f migrations/002_seed_data.sql -U postgres"
echo ""

# Start API server
echo "🌐 Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "API Docs at: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

