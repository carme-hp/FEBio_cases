#!/bin/bash

results_dir="results-opendihu-opendihu"
mkdir -p "$results_dir"

echo "Saving results to $results_dir..."
mv precice-run/ "$results_dir" 2>/dev/null
mv precice-output/ "$results_dir" 2>/dev/null

# move results from fibers participant
mv fibers-opendihu/results/ "$results_dir"/fibers-results 2>/dev/null
mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers-precice 2>/dev/null

# move results from mechanics participant
mv mechanics-opendihu/results/ "$results_dir"/muscle-results 2>/dev/null
mv mechanics-opendihu/precice-profiling/ "$results_dir"/muscle-precice 2>/dev/null

echo "Results saved to $results_dir"

