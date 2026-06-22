#!/usr/bin/env bash
set -e -u

echo "Cleaning subfolders..."
(cd fibers-opendihu && ./clean.sh)
(cd mechanics-febio && ./clean.sh)
(cd mechanics-opendihu && ./clean.sh)

echo "Cleaning main directory..."
rm -rf precice-run precice-output
rm -rf results-opendihu-fibers results-opendihu-muscle

echo "Clean complete!"