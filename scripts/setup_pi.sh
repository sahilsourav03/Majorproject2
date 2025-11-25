#!/usr/bin/env bash
# Setup script for Raspberry Pi 4B
# Run this once after cloning the repository

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=== Raspberry Pi 4B Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Fix indentation issues
echo "Fixing any indentation issues..."
python3 scripts/fix_indentation.py

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.sh
chmod +x scripts/*.py

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To run the project:"
echo "  source .venv/bin/activate"
echo "  ./scripts/run.sh"
echo ""
echo "Or:"
echo "  python3 -m src.crack_detector.main --config configs/default.yaml"

