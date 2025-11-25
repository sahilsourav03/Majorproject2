#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Auto-fix indentation issues before running
if [ -f "scripts/fix_indentation.py" ]; then
    python3 scripts/fix_indentation.py > /dev/null 2>&1 || true
fi

# Run the main application
python3 -m src.crack_detector.main "$@"
