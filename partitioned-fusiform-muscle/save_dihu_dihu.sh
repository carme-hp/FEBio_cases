#!/bin/bash

results_dir="results-opendihu-opendihu"
mkdir -p "$results_dir"

echo "Saving results to $results_dir..."
mv results-opendihu-fibers/ "$results_dir/fibers-solver" 2>/dev/null
mv results-opendihu-muscle/ "$results_dir/muscle-solver" 2>/dev/null
mv precice-output/ "$results_dir" 2>/dev/null

mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers-precice 2>/dev/null
mv mechanics-opendihu/precice-profiling/ "$results_dir"/muscle-precice 2>/dev/null

echo "Results saved to $results_dir"

