import pyvista as pv
import numpy as np

fine = pv.read("results_results116/results-opendihu-muscle/muscle_0000299.vtu")
coarse = pv.read("results_results102/results-opendihu-muscle/muscle_0000299.vtu")

# interpolate coarse field onto fine mesh
coarse_on_fine = fine.sample(coarse)

u_fine = fine["u"]
u_coarse = coarse_on_fine["u"]

# validity mask
mask = coarse_on_fine["vtkValidPointMask"] == 1

u_fine = u_fine[mask]
u_coarse = u_coarse[mask]

diff = u_fine - u_coarse

# squared vector norm
err2 = np.sum(diff**2, axis=1)

# point volumes / weights
volumes = np.abs(fine.compute_cell_sizes()["Volume"])


# crude nodal weighting
h = np.mean(  volumes)

L2_err = np.sqrt(np.sum(err2) * h)

ref2 = np.sum(u_fine**2, axis=1)
L2_ref = np.sqrt(np.sum(ref2) * h)

print("relative error =", L2_err / L2_ref)