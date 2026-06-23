#!/usr/bin/env bash
set -e -u

# Run coupled OpenDiHu-FEBio simulation
# NOTE: Both solvers must run in separate terminals simultaneously for preCICE coupling to work

echo "========================================"
echo "OpenDiHu-FEBio Coupled Simulation"
echo "========================================"
echo ""
echo ""
echo "Launch fibers-opendihu:"
cd fibers-opendihu && . run.sh &
echo ""
echo "Launch mechanics-febio:"
cd mechanics-febio && . run.sh &
echo ""
echo "========================================"
echo "Waiting for simulations to complete..."
wait
echo "✓ All simulations completed!"
