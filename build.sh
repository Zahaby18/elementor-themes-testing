#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Rebuilding templates..."
python3 build.py

echo "==> Zipping kit..."
rm -f kit.zip
zip -r kit.zip content templates > /dev/null

echo "==> Done: kit.zip ($(du -h kit.zip | cut -f1))"
