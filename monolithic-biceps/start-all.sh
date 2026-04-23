source ../../darus_setup.sh

cd build_release
rm -r precice-run
echo "Launching muscle mechanics"
mpirun -n 1 ./muscle_contraction ../settings_muscle_mechanics.py ramp.py --case_name "ramp" &>mechanics.log &
echo "Launching muscle fibers"
mpirun -n 16 ./muscle_fibers ../settings_muscle_fibers.py ramp.py --case_name "ramp" &>fibers.log &
echo "Launching tendon bottom"
mpirun -n 1 ./tendon ../settings_tendon_bottom.py ramp.py --case_name "ramp" &>bottom.log &
echo "Launching tendon top-a"
mpirun -n 1 ./tendon_linear ../settings_tendon_top_a.py ramp.py --case_name "ramp" &>top_a.log &
echo "Launching tendon top-b"
mpirun -n 1 ./tendon_linear ../settings_tendon_top_b.py ramp.py --case_name "ramp" &>top_b.log
cd ..
