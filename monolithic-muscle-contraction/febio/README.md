# Monolithic Muscle Contraction - FEBio Simulation Hub

This directory serves as the execution hub for the ready-to-run finite element input files (`.feb`) modeling active skeletal muscle contraction. It isolates the dynamic simulation parameters, continuum physics settings, and solver configurations from the underlying raw geometric assets.

## Core Objective
The models housed here simulate dynamic, active muscle contraction under physiological electrical signals across various idealized and biological shapes to analyze geometric deformation, internal stress fields, and mechanical behavior.

---

## Directory Inventory

| File / Folder | Type | Description |
| :--- | :--- | :--- |
| **`geometry_and_mesh_details/`** | Directory | Asset library containing raw shapes (`.stl`) and detailed volumetric meshing specifications. |
| **`cylinder_Activecontraction.feb`** | FEBio Input | Idealized cylindrical model used to verify the dynamic active contraction pipeline. |
| **`cuboid-muscle-contraction.feb`** | FEBio Input | Idealized rectangular prism reference case demonstrating directional contraction. |
| **`ellipsoid-muscle-contraction.feb`** | FEBio Input | Idealized spindle-shaped reference case tracking non-uniform contraction. |
| **`biceps-smooth-contraction.feb`** | FEBio Input | Reference model showcasing contraction on a smooth, continuous muscle layout. |
| **`TA_poisson.feb`** | FEBio Input | Biological Tibialis Anterior model using a high-density mesh optimized via Poisson surface reconstruction. |

---

## Shared Simulation Physics & Solver Baseline

To maintain a clean repository structure and eliminate descriptive redundancy, all five simulation files in this directory utilize an identical mathematical, material, and solver blueprint:

### 1. Continuum Mechanics & Material Architecture
* **Passive Ground Matrix:** Formulated as an **Uncoupled Transversely Isotropic Mooney-Rivlin** hyperelastic material ($c_1 = 13.85$, $c_2 = 0.0$, $c_3 = 2.07$, $c_4 = 61.44$, $c_5 = 640.7$, bulk modulus $k = 100.0$, and structural stretch limit $\lambda_{\text{max}} = 1.03$).
* **Fiber Alignment:** Biological muscle striations are uniformly oriented along the global Z-axis vector (`[0, 0, 1]`).
* **Active Contraction Model:** Force generation is driven by a physiological length-tension active model ($ca_0 = 4.35$, $\beta = 4.75$, $l_0 = 1.58$, $refl = 2.04$). The contraction is modulated by a master activation scale (`ascl`) wired to a piecewise ramping load curve (`LC1`).

### 2. Time-Dependent Solver Configuration
* **Analysis Type:** `DYNAMIC` solid mechanics solver explicitly factoring in tissue density ($\rho = 1.0$) and mass inertia effects.
* **Time Discretization:** Configured for exactly `300` time steps with a step size of `0.1` seconds, capturing a total physiological time window of $30.0\text{ s}$.
* **Matrix Math:** Utilizes a full `symmetric` stiffness matrix with quasi-Newton BFGS updates for stable non-linear equilibrium iterations.

---

## Local Execution Quick Start

To execute any of these simulation files locally via the FEBio command-line interface, ensure your terminal is inside this directory and call the solver using the standard input flag format shown below.

```bash
febio4 -i cylinder_Activecontraction.feb
```

Note: The command below uses cylinder_Activecontraction.feb as a baseline example. It can be replaced with any of the other .feb files listed in the directory inventory to run their respective simulations.