#!/bin/bash
set -e

echo "🚀 Orchestrator Dashboard Setup"
echo "================================"

# Check system dependencies
echo "✓ Checking dependencies..."
command -v python3 >/dev/null || { echo "❌ Python 3 required"; exit 1; }
command -v git >/dev/null || { echo "❌ Git required"; exit 1; }

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r projects/dashboard/requirements.txt

# Initialize database
echo "✓ Initializing database..."
python3 << 'PYEOF'
import sys
sys.path.insert(0, 'projects/dashboard')
from database import init_db
init_db()
print("✓ Database initialized")
PYEOF

# Copy environment template
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✓ Created .env (edit as needed)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run dashboard: python3 projects/dashboard/app.py"
echo "  3. Open browser: http://localhost:5000"
echo "  4. Run tests: pytest projects/dashboard/tests/"
