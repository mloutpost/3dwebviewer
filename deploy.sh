#!/usr/bin/env bash
# Deploy shoptimberframekits.com (site + Cloud Functions)
# Run from this repo root. Uses lctf_clients for Firebase deploy.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LCTF_CLIENTS="${SCRIPT_DIR}/../lctf_clients"
if [[ ! -d "$LCTF_CLIENTS" ]]; then
  echo "Error: lctf_clients not found at $LCTF_CLIENTS"
  exit 1
fi
cd "$LCTF_CLIENTS"
firebase deploy --only hosting:viewer,functions
