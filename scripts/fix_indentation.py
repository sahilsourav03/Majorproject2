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
    
    Also normalizes line endings and removes trailing whitespace.
    Returns True if tabs were found and fixed, False otherwise.
    """
    try:
        # Read as binary to preserve exact content
        content = filepath.read_bytes()
        original_content = content
        
        # Convert tabs to 4 spaces
        if b'\t' in content:
            content = content.replace(b'\t', b'    ')
        
        # Normalize line endings to Unix (LF only)
        content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        
        # Remove trailing whitespace from each line
        lines = content.split(b'\n')
        cleaned_lines = []
        for line in lines:
            # Remove trailing spaces/tabs but keep the newline structure
            cleaned_line = line.rstrip(b' \t')
            cleaned_lines.append(cleaned_line)
        content = b'\n'.join(cleaned_lines)
        
        # Only write if something changed
        if content != original_content:
            filepath.write_bytes(content)
            print(f"✓ Fixed: {filepath}")
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

