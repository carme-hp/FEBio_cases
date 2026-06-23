#!/usr/bin/env bash
set -e -u

# Build if necessary
if [ ! -f ./build_release/muscle ]; then
  mkorn && sr
fi

./build_release/muscle settings_muscle.py 0 1 2>&1 | tee mechanics_opendihu.log
