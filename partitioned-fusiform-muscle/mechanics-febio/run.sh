#!/usr/bin/env bash
set -e -u
FILE="${1:-fusiform-muscle-unstructured.feb}"
mpirun -n 1 ~/FEBioStudio/bin/febio4 "$FILE" 2>&1 | tee mechanics_febio.log

