#!/usr/bin/env bash
set -e -u
echo "Cleaning subfolders..."
for dir in fibers-opendihu mechanics-febio mechanics-opendihu; do
  if [[ -f "$dir/clean.sh" ]]; then
    echo "Running $dir/clean.sh..."
    (cd "$dir" && bash clean.sh)
  fi
done

echo "Cleaning main directory..."
rm -r results-opendihu-opendihu results-opendihu-febio precice-output precice-run


echo "Clean complete!"