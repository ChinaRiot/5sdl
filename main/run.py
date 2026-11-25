#!/usr/bin/env python3


import subprocess
import sys
from pathlib import Path

def run_command(script, description):
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"{'='*60}")
    
    result = subprocess.run([sys.executable, script], cwd=Path(__file__).parent)
    
    if result.returncode != 0:
        print(f"ERROR: {script} failed with exit code {result.returncode}")
        return False
    return True

def main():
    print("\nwork start")
    print("=" * 60)
    
    list_file = Path(__file__).parent / "list.txt"
    if not list_file.exists():
        print("ERROR: list.txt not found")
        print("\nCheck formatting")
        sys.exit(1)
    
    if not run_command("parse.py", "Parse list.txt -> data.json"):
        sys.exit(1)
    
    if not run_command("generate.py", "Generate data.json -> index.html"):
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("done")
    print(f"{'='*60}")
    print("\nGenerated files:")
    print("data.json")
    print("index.html")

if __name__ == "__main__":
    main()
