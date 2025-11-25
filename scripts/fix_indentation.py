#!/usr/bin/env python3
"""Fix tab/space indentation issues in Python files.

This script converts all tabs to spaces (4 spaces per tab) in all Python files.
Run this if you encounter TabError when running the project.
"""

import os
import sys
from pathlib import Path


def fix_tabs_in_file(filepath: Path) -> bool:
    """Convert tabs to spaces (4 spaces per tab) in a Python file.
    
    Returns True if tabs were found and fixed, False otherwise.
    """
    try:
        content = filepath.read_bytes()
        
        # Check if file has tabs
        if b'\t' in content:
            # Convert tabs to 4 spaces
            new_content = content.replace(b'\t', b'    ')
            filepath.write_bytes(new_content)
            print(f"✓ Fixed tabs in: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}", file=sys.stderr)
        return False


def main():
    """Find and fix all Python files with tab indentation."""
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    
    if not src_dir.exists():
        print(f"Error: {src_dir} not found. Are you in the project root?")
        sys.exit(1)
    
    fixed_count = 0
    for py_file in src_dir.rglob("*.py"):
        if fix_tabs_in_file(py_file):
            fixed_count += 1
    
    if fixed_count == 0:
        print("✓ No tabs found in Python files. All files use spaces for indentation.")
    else:
        print(f"\n✓ Fixed {fixed_count} file(s). You can now run the project.")


if __name__ == "__main__":
    main()

