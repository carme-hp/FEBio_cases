import pyvista as pv
import numpy as np

fine = pv.read("results_16x16x64/results-opendihu-muscle/muscle_0000299.vtu")
coarse = pv.read("results_8x8x32/results-opendihu-muscle/muscle_0000299.vtu")

print("fine:", fine.n_points, "coarse:", coarse.n_points)
print("fine cells:", fine.n_cells, "coarse cells:", coarse.n_cells)

# fine = fine.point_data_to_cell_data()
# coarse = coarse.point_data_to_cell_data()


# Interpolate coarse solution onto fine mesh
coarse_on_fine = fine.sample(coarse)

u_fine = fine.point_data["u"]
u_coarse_interp = coarse_on_fine.point_data["u"]

print(coarse_on_fine["u"].shape)
print(fine["u"].shape)
print("max u_fine:", np.max(u_fine))
print("max u_coarse_interp:", np.max(u_coarse_interp))
# Difference
diff_cell = u_fine - u_coarse_interp
error_cell = np.sum(diff_cell**2, axis=1)
print("max diff_cell:", np.max(diff_cell))
print("max error_cell:", np.max(error_cell))

# Reference norm (fine solution)

fine_cell = fine.point_data_to_cell_data()
coarse_interp_cell = coarse_on_fine.point_data_to_cell_data()

u_fine = fine_cell["u"]
u_coarse = coarse_interp_cell["u"]

diff = u_fine - u_coarse
error_cell = np.sum(diff**2, axis=1)

volumes = np.abs(fine_cell.compute_cell_sizes()["Volume"])

L2_err = np.sqrt(np.sum(error_cell * volumes))
ref = np.sum(u_fine**2, axis=1)
L2_ref = np.sqrt(np.sum(ref * volumes))

print("L2 error:", L2_err)
print("Relative error:", L2_err / L2_ref)

