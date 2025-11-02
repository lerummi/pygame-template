#!/usr/bin/env python3
"""
Python syntax and basic runtime validator for build process
Validates all .py files in the app directory
"""
import sys
import ast
import traceback
from pathlib import Path

def validate_file(filepath):
    """Validate a single Python file for syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source, filename=str(filepath))
        return True
    except SyntaxError as e:
        print(f"\n{filepath}:{e.lineno}:{e.offset}: SyntaxError: {e.msg}")
        if e.text:
            print(f"  {e.text.rstrip()}")
            if e.offset:
                print(f"  {' ' * (e.offset - 1)}^")
        return False
    except Exception as e:
        print(f"\n{filepath}: Error: {e}")
        return False

def check_runtime_errors(filepath):
    """Try to compile and check for basic runtime errors"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        # Compile the code (this catches some errors that ast.parse doesn't)
        compile(source, str(filepath), 'exec')
        return True
    except SyntaxError as e:
        # Already caught by validate_file
        return False
    except NameError as e:
        print(f"\n{filepath}: NameError: {e}")
        return False
    except Exception as e:
        # Show the full traceback for other errors
        print(f"\n{filepath}: {type(e).__name__}: {e}")
        traceback.print_exc()
        return False

def main():
    app_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "app")

    if not app_dir.exists():
        print(f"Error: Directory {app_dir} not found")
        sys.exit(1)

    python_files = list(app_dir.glob("*.py"))

    if not python_files:
        print(f"No Python files found in {app_dir}")
        sys.exit(0)

    all_valid = True
    for pyfile in python_files:
        # Check syntax
        if not validate_file(pyfile):
            all_valid = False
            continue

        # Check for basic runtime errors
        if not check_runtime_errors(pyfile):
            all_valid = False

    if not all_valid:
        sys.exit(1)

if __name__ == "__main__":
    main()
