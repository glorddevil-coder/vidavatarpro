# Development startup script for AuraStudio Omni - Windows (PowerShell)
# Run with: .\dev-start.ps1

Write-Host "🚀 AuraStudio Omni - Development Startup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "✓ Checking Python installation..." -ForegroundColor Cyan
python --version

# Create virtual environment if not exists
if (-not (Test-Path "venv")) {
    Write-Host "✓ Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "✓ Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "✓ Installing dependencies..." -ForegroundColor Cyan
pip install -r api/requirements.txt -q

# Create .env if not exists
if (-not (Test-Path ".env.development")) {
    Write-Host "⚠️  Creating .env.development (please configure with real keys)" -ForegroundColor Yellow
    Copy-Item ".env.development.example" ".env.development" -ErrorAction SilentlyContinue
}

# Database setup info
Write-Host ""
Write-Host "📦 Database Setup (optional - requires PostgreSQL)" -ForegroundColor Yellow
Write-Host "To set up database, run:" -ForegroundColor Yellow
Write-Host "  cd db" -ForegroundColor Gray
Write-Host "  psql -f migrations/001_initial_schema.sql -U postgres" -ForegroundColor Gray
Write-Host "  psql -f migrations/002_seed_data.sql -U postgres" -ForegroundColor Gray
Write-Host ""

# Start API server
Write-Host "🌐 Starting FastAPI server..." -ForegroundColor Green
Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs at: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location api
& uvicorn main:app --host 0.0.0.0 --port 8000 --reload

