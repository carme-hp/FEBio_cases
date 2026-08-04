# Monolithic Muscle Contraction - FEBio Simulation Hub

This directory serves as the execution hub for the ready-to-run finite element input files (`.feb`) modeling active skeletal muscle contraction. It isolates the dynamic simulation parameters, continuum physics settings, and solver configurations from the underlying raw geometric assets.

## Core Objective
The models housed here simulate dynamic, active muscle contraction under physiological electrical signals across various idealized and realistic muscle shapes to analyze geometric deformation, internal stress fields, and mechanical behavior.

---

## Directory Inventory

| File / Folder | Type | Description |
| :--- | :--- | :--- |
| **`geometry_and_mesh_details/`** | Directory | Asset library containing raw shapes (`.stl`) and detailed volumetric meshing specifications. |
| **`cylinder-muscle-contraction.feb`** | FEBio Input | Idealized cylindrical model used to verify the dynamic active contraction pipeline. |
| **`cuboid-muscle-contraction.feb`** | FEBio Input | Idealized rectangular prism reference case demonstrating directional contraction. |
| **`ellipsoid-muscle-contraction.feb`** | FEBio Input | Idealized spindle-shaped reference case tracking non-uniform contraction. |
| **`biceps-muscle-contraction.feb`** | FEBio Input | Reference model showcasing contraction on a realistic biceps geometry. |
| **`TA-muscle-contraction.feb`** | FEBio Input | Biological Tibialis Anterior model showcasing contraction on a realistic muscle geometry. |

---

## Shared Simulation Physics & Solver Baseline
To maintain a clean repository structure and eliminate descriptive redundancy, all five simulation files in this directory utilize an identical mathematical, material, and solver blueprint. A comprehensive parameter sensitivity analysis of this shared material and solver configuration was conducted on the biceps model — see the [Biceps Muscle Contraction Parameter Study](https://github.com/gowtham2598/biceps_contraction/tree/parameter-study) repository for full documentation.

### 1. Continuum Mechanics & Material Architecture
* **Passive Ground Matrix:** Formulated as an **Uncoupled Transversely Isotropic Mooney-Rivlin** hyperelastic material ($c_1 = 13.85$, $c_2 = 0.0$, $c_3 = 2.07$, $c_4 = 61.44$, $c_5 = 640.7$, bulk modulus $k = 100.0$, and structural stretch limit $\lambda_{\text{max}} = 1.03$).
* **Fiber Alignment:** Biological muscle striations are uniformly oriented along the global Z-axis vector (`[0, 0, 1]`).
* **Active Contraction Model:** Force generation is driven by a physiological length-tension active model ($ca_0 = 4.35$, $\beta = 4.75$, $l_0 = 1.58$, $refl = 2.04$). The contraction is modulated by a master activation scale (`ascl`) wired to a piecewise ramping load curve (`LC1`).

### 2. Time-Dependent Solver Configuration
* **Analysis Type:** `DYNAMIC` solid mechanics solver using **implicit time integration** (FEBio default `solid` solver, per FEBio User Manual Section 8.4.1), explicitly factoring in tissue density ($\rho = 1.0$) and mass inertia effects.
* **Time Discretization:** Configured for exactly `300` time steps with a step size of `0.1` seconds, capturing a total physiological time window of $30.0\text{ s}$.
* **Solver Type:** Utilizes a full `symmetric` stiffness matrix with quasi-Newton BFGS updates for stable non-linear equilibrium iterations.

---

## Local Execution Quick Start

To execute any of these simulation files locally via the FEBio command-line interface, ensure your terminal is inside this directory and call the solver using the standard input flag format shown below.

```bash
febio4 -i cylinder_Activecontraction.feb
```

Note: The command below uses cylinder_Activecontraction.feb as a baseline example. It can be replaced with any of the other .feb files listed in the directory inventory to run their respective simulations.

---

## Output Data Extraction

### What Gets Saved, and How
Which fields FEBio writes out is controlled by the `<Output>` block in the `.feb` XML. This can be configured either through FEBioStudio's GUI or by directly editing the `.feb` file — either way, it comes down to the same underlying `<Output>` block, since FEBioStudio itself just writes to that XML. FEBio's documentation lists a large set of exportable variables; the ones most relevant to this pipeline are **displacement**, **stress**, **fiber_stretch**, **relative volume**, **Lagrange strain**, and **pressure**.

### Why Nodal Conversion Is Needed
Fields like stress, strain, and fiber_stretch are computed by FEBio's solver at internal integration (Gauss) points inside each element — not at the mesh nodes. Since nodal displacement (the primary solved variable) naturally lives at the nodes, any workflow that wants these other fields aligned with the same nodal mesh structure — e.g. for surrogate model datasets — needs a conversion step from element/integration-point data to nodal data.

FEBio offers three distinct approaches to this:

| Method | Approach | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Simple averaging** | Average an element's integration-point values into one number, then average across elements sharing a node | Simple, robust, field-agnostic | Discards internal gradients within an element |
| **Shape-function extrapolation** (`nodal stress`, `nodal strain`) | Extrapolate each element's own Gauss-point values to its nodes using its shape functions, then average across elements | Captures internal gradients per element | Only available for a limited, pre-defined set of fields |
| **SPR** (`SPR stress`, `SPR-P1 stress`, `SPR relative volume`, `SPR Lagrange strain`, etc.) | Fit a least-squares polynomial across all Gauss-point values in the patch of elements surrounding a node | Generally the most accurate, especially for higher-order elements | Also limited to specific pre-defined fields; can be ill-conditioned on thin/single-element-thick geometry (FEBio offers `SPR-P1` for this case) |

### What This Repo Uses
Since `fiber_stretch` and `pressure` have no native FEBio `nodal_*` or `SPR_*` equivalent, this pipeline uses a custom, field-agnostic script (`custom_nodal_conversion.py`) that replicates the simple-averaging approach in Python, working identically across any element-based field. It was validated against FEBio's native `nodal_stress` output for the stress field, with agreement at the level of float32 storage precision.

Note: while this simple-averaging script works across all element types, FEBio's native extrapolation and SPR methods can be more accurate for higher-order elements like TET10, where multiple integration points capture internal gradients that simple averaging discards.