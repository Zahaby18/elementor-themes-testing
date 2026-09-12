#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Rebuilding templates and kit..."
python3 build.py

echo "==> Zipping kit..."
rm -f kit.zip
(cd kit && zip -qr ../kit.zip manifest.json content)

echo "==> Done: kit.zip ($(du -h kit.zip | cut -f1))"
