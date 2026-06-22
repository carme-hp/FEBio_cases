#!/bin/bash

results_dir="results-opendihu-febio"
mkdir -p "$results_dir"

echo "Saving results to $results_dir..."
mv results-opendihu-fibers/ "$results_dir/fibers-solver" 2>/dev/null
mv mechanics-febio/*.xplt "$results_dir/muscle-solver" 2>/dev/null
mv precice-output/ "$results_dir" 2>/dev/null

mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers-precice 2>/dev/null
mv mechanics-febio/precice-profiling/ "$results_dir"/febio-precice 2>/dev/null

echo "Results saved to $results_dir"

