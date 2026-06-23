#!/bin/bash

results_dir="results-opendihu-febio"
mkdir -p "$results_dir"

echo "Saving results to $results_dir..."
mv precice-output/ "$results_dir" 2>/dev/null

# move results from fibers participant
mv fibers-opendihu/results/ "$results_dir"/fibers-results 2>/dev/null
mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers-precice 2>/dev/null
# move results from mechanics participant
mv mechanics-febio/*.xplt "$results_dir/muscle-solver" 2>/dev/null
mv mechanics-febio/precice-profiling/ "$results_dir"/febio-precice 2>/dev/null

echo "Results saved to $results_dir"

