# Muscle Surface Data and Mesh Specifications

This directory contains surface mesh assets (`.stl`) used to generate the volumetric meshes for the active muscle contraction studies, separating surface geometry from downstream simulation parameters (such as material models, boundary conditions, and solver settings).

The 3D volumetric finite element meshes generated from these surfaces are embedded directly in the `.feb` simulation files located in the parent directory (`../cylinder-muscle-contraction.feb` and `../TA-muscle-contraction.feb`).

---

## Standard Geometry & Meshing Pipeline

To ensure high-quality finite element simulations and avoid structural artifacts during large hyperelastic deformations, geometries in this folder are preprocessed using one of the following workflows depending on the geometry source:

**Workflow A — CAD-exported idealized geometries:**
1. **Surface Remeshing (MMG Remesh):** Raw CAD surface shells (`.stl` files) are processed using the MMG Remesh tool within FEBioStudio, redistributing irregular faces into a uniform boundary triangular mesh to prepare for stable volumetric packing.
2. **Volumetric Packing (TetGen):** The TetGen integration utility within FEBioStudio fills the enclosed interior volume with solid tetrahedral elements, translating the surface shell into a continuous continuum domain.

**Workflow B — Segmented biological geometries:**
1. **Surface Remeshing (Blender / MeshLab):** Segmented biological surface meshes are cleaned, smoothed, and remeshed using Blender and MeshLab prior to import into FEBioStudio.
2. **Volumetric Packing (TetGen):** Same TetGen step as Workflow A is applied within FEBioStudio to fill the enclosed surface shell with solid tetrahedral elements.

---

## 1. Skeletal Muscle Cylinder (Idealized Geometry)

### Geometric Profile
* **Description:** A simplified, scratch-built cylindrical representation of skeletal muscle tissue used to test and verify the structural finite element pipeline.
* **Dimensions:** Diameter $\emptyset = \text{10 mm}$, Length $L = \text{20 mm}$.

### Mesh Architecture
The raw CAD surface shell (`cylinder_test.stl`) was remeshed to 3,550 boundary faces via MMG (Element Size: 0.8) and volumetrically packed using TetGen. It utilizes quadratic elements to explicitly prevent volumetric locking under near-incompressible material formulations. The resulting volumetric mesh is embedded in `../cylinder-muscle-contraction.feb`.

| Metric | Specification |
| :--- | :--- |
| **Surface File (this directory)** | `cylinder_test.stl` |
| **Surface Faces** | 3,550 |
| **Volumetric Model (parent directory)** | `../cylinder-muscle-contraction.feb` |
| **Element Type** | TET10 (Quadratic Tetrahedron) |
| **Total Elements** | 33,546 |
| **Total Nodes** | 47,684 |

---

## 2. Tibialis Anterior (Biological Geometry)

### Geometric Profile
* **Description:** A realistic biological muscle geometry mapping the complex, organic structure of the Tibialis Anterior (TA) muscle. 

### Mesh Architecture
The surface mesh (`TA_poisson.stl`) was cleaned and smoothed using Poisson surface reconstruction and volumetrically packed into linear tetrahedral elements using TetGen. The resulting volumetric mesh is embedded in `../TA-muscle-contraction.feb`.

| Metric | Specification |
| :--- | :--- |
| **Surface File (this directory)** | `TA_poisson.stl` |
| **Surface Faces** | 51,616 |
| **Volumetric Model (parent directory)** | `../TA-muscle-contraction.feb` |
| **Element Type** | TET4 (Linear Tetrahedron) |
| **Total Elements** | 196,956 |
| **Total Nodes** | 44,597 |
