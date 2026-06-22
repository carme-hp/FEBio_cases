#!/usr/bin/env bash
set -u

# Script to run 5 coupled simulations
# Each iteration runs muscle and fibers simulations in parallel, then saves results

# Don't exit on error - handle it manually instead
set +e

# Run simulation 5 times with different tags
for i in {1..5}; do
    echo "=========================================="
    echo "Running simulation iteration $i"
    echo "=========================================="
    
    # Define the tag for this run
    TAG="rbf4x4x16_${i}"
    
    # Start the muscle simulation in background
    (cd mechanics-opendihu && ./build_release/muscle settings_muscle.py) &
    MUSCLE_PID=$!
    
    # Start the fibers simulation in background
    (cd fibers-opendihu && ./build_release/fibers settings_fibers.py) &
    FIBERS_PID=$!
    
    # Wait for both simulations to complete
    echo "Waiting for muscle (PID: $MUSCLE_PID) and fibers (PID: $FIBERS_PID) simulations to complete..."
    wait $MUSCLE_PID
    MUSCLE_STATUS=$?
    wait $FIBERS_PID
    FIBERS_STATUS=$?
    
    if [ $MUSCLE_STATUS -ne 0 ]; then
        echo "✗ ERROR: Muscle simulation failed with exit code $MUSCLE_STATUS"
        exit 1
    fi
    if [ $FIBERS_STATUS -ne 0 ]; then
        echo "✗ ERROR: Fibers simulation failed with exit code $FIBERS_STATUS"
        exit 1
    fi
    
    echo "✓ Simulations completed successfully"
    
    # Run the save script with the tag as input
    echo "Moving results with tag: $TAG"
    echo "$TAG" | . save_dihu_dihu.sh
    SAVE_STATUS=$?
    if [ $SAVE_STATUS -ne 0 ]; then
        echo "✗ ERROR: Save script failed with exit code $SAVE_STATUS"
        exit 1
    fi
    
    echo "✓ Iteration $i completed"
    echo ""
done

echo "=========================================="
echo "✓ All 5 iterations completed successfully!"
echo "=========================================="
