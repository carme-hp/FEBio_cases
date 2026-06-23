#!/usr/bin/env bash
set -e -u

echo "========================================"
echo "OpenDiHu-OpenDiHu Coupled Simulation"
echo "========================================"
echo ""
echo ""
echo "Launching fibers-opendihu:"
cd fibers-opendihu && . run.sh &
echo ""
echo "Launching mechanics-opendihu:"
cd mechanics-opendihu && . run.sh &
echo ""
echo "========================================"
echo "Waiting for simulations to complete..."
wait
echo "✓ All simulations completed!"
