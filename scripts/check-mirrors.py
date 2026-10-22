#!/usr/bin/env python3
"""Check application source shared by the Xcode and SwiftPM packages."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
folders = ("App", "Debug", "Engine", "Features", "Models", "Parsing", "Theory")
errors = []
checked = 0
for folder in folders:
    left = root / "ImprovBuddy" / folder
    right = root / "Jade.swiftpm" / folder
    if not left.is_dir() or not right.is_dir():
        errors.append(f"Missing mirrored directory: {folder}")
        continue
    left_files = {p.relative_to(left) for p in left.rglob("*") if p.is_file()}
    right_files = {p.relative_to(right) for p in right.rglob("*") if p.is_file()}
    for path in sorted(left_files | right_files):
        if path not in left_files or path not in right_files:
            errors.append(f"Missing mirrored file: {folder}/{path}")
        elif (left / path).read_bytes() != (right / path).read_bytes():
            errors.append(f"Different mirrored file: {folder}/{path}")
        checked += 1
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"Mirrored application sources match: {checked} files.")
