#!/bin/bash

# Ask for user input
read -p "Enter name for results file: " id

results_dir="results_febio_rbf_v2_$id"
mkdir -p "$results_dir"

mv results-opendihu-fibers/ "$results_dir"
mv mechanics-febio/fusiform-muscle-"$id"_v2.xplt "$results_dir"
mv precice-output/ "$results_dir"


mv fibers-opendihu/precice-profiling/ "$results_dir"/fibers
mv mechanics-febio/precice-profiling/ "$results_dir"/muscle

