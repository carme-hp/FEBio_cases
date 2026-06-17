#!/bin/bash

# Script to process precice profiling data for simulation results
# Runs precice-cli profiling merge and export on all results directories

# Define the tag patterns to process
TAGS=("2x2x8_" "4x4x16_" "8x8x32_")

echo "=========================================="
echo "Processing precice profiling data"
echo "=========================================="
echo ""

# Counter for processed directories
PROCESSED=0

# Process each tag pattern
for TAG in "${TAGS[@]}"; do
    echo "Looking for directories with tag: ${TAG}*"
    
    # Find all directories matching the pattern
    for dir in results_${TAG}*; do
        # Check if directory exists (glob might not match anything)
        if [ -d "$dir" ]; then
            echo ""
            echo "=========================================="
            echo "Processing: $dir"
            echo "=========================================="
            
            # Navigate to the directory
            cd "$dir"
            
            # Run precice profiling commands
            echo "Running: precice-cli profiling merge"
            precice-cli profiling merge
            
            echo "Running: precice-cli profiling export"
            precice-cli profiling export
            
            echo "✓ Completed processing $dir"
            
            # Go back to parent directory
            cd ..
            
            ((PROCESSED++))
        fi
    done
done

echo ""
echo "=========================================="
echo "✓ Processing complete!"
echo "✓ Processed $PROCESSED directories"
echo "=========================================="
