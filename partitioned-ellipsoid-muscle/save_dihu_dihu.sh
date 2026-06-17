#!/bin/bash

# Ask for user input
read -p "Enter name for results file: " id

results_dir="results_$id"
mkdir -p "$results_dir"

mv results-opendihu-fibers/ "$results_dir"
mv results-opendihu-muscle/ "$results_dir"
mv precice-output/ "$results_dir"


mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers
mv mechanics-opendihu/precice-profiling/ "$results_dir"/muscle

