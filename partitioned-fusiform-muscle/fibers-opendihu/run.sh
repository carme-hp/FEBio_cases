#!/usr/bin/env bash
set -e -u

# Build if necessary
if [ ! -f ./build_release/fibers ]; then
  mkorn && sr
fi

./build_release/fibers settings_fibers.py 0 1 2>&1 | tee fibers_opendihu.log
