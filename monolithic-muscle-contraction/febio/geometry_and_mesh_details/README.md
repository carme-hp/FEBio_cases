# Muscle Geometry and Volumetric Mesh Specifications

This directory serves as the dedicated asset repository for the physical shapes and volumetric finite element meshes used in these muscle contraction studies. It contains raw geometric surface data and processed mesh files, separating physical shape attributes from downstream simulation parameters (such as material models, boundary conditions, and solver settings).

---

## Standard Geometry & Meshing Pipeline

To ensure high-quality finite element simulations and avoid structural artifacts during large hyperelastic deformations, all geometries in this folder follow a consistent, two-step surface-to-volume preprocessing workflow within FEBioStudio:

1. **Surface Remeshing (MMG Remesh):** Raw CAD or segmented biological surface shells (typically `.stl` files) are processed using the MMG Remesh tool. This step artificial shatters irregular or large CAD faces into a highly uniform, optimized boundary triangular web to prepare for stable volumetric packing.
2. **Volumetric Packing (TetGen):** With surface constraints uniform, the TetGen integration utility is utilized to fill the enclosed interior volume with solid tetrahedral elements, translating a hollow shell into a continuous continuum domain.

---

## 1. Skeletal Muscle Cylinder (Idealized Geometry)

### Geometric Profile
* **Description:** A simplified, scratch-built cylindrical representation of skeletal muscle tissue used to test and verify the structural finite element pipeline.
* **Dimensions:** Diameter $\emptyset = \text{10 mm}$, Length $L = \text{20 mm}$.

### Mesh Architecture
The cylinder surface was remeshed to 3,550 boundary faces via MMG (Element Size: 0.8) and volumetrically packed using TetGen. It utilizes quadratic elements to explicitly prevent volumetric locking under near-incompressible material formulations.

| Metric | Specification |
| :--- | :--- |
| **Primary File** | `cylinder_test.stl` |
| **Element Type** | TET10 (Quadratic Tetrahedron) |
| **Total Elements** | 33,546 |
| **Total Nodes** | 47,684 |
| **Surface Faces** | 3,550 |

---

## 2. Tibialis Anterior (Biological Geometry)

### Geometric Profile
* **Description:** A realistic biological muscle geometry mapping the complex, organic structure of the Tibialis Anterior (TA) muscle. 

### Mesh Architecture
Due to the highly intricate surface features of the biological muscle, a significantly denser mesh resolution is required to capture the anatomical curves accurately without element distortion.

| Metric | Specification |
| :--- | :--- |
| **Primary File** | `TA_poisson.feb` (Mesh-Only) |
| **Element Type** | TET4 (Linear Tetrahedron) |
| **Total Elements** | 196,956 |
| **Total Nodes** | 44,597 |
| **Surface Faces** | 51,616 |