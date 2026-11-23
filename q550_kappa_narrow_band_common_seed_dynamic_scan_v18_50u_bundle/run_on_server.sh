#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
PYTHON_BIN="${PYTHON_BIN:-python3.13}"
"$PYTHON_BIN" scripts/verify_source_manifest.py
"$PYTHON_BIN" tests/test_audit_rules.py
"$PYTHON_BIN" scripts/run_audit.py "$@"
"$PYTHON_BIN" scripts/write_output_manifest.py
"$PYTHON_BIN" scripts/pack_sendback.py
