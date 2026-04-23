# Mechanics Mesh Generation

The requirements on the mechanics mesh depend on our solver of choice. 
- OpenDiHu requires an hexahedral structural mesh. Non-cubic meshes are provided via an input `.vtk` file. 
- TODO: FEBio supports many mesh formats. The mesh is included in the `.feb` configuration file that is created with FEBioStudio. 

**Challenge:** The mechanics and the fibers mesh should overlap. This means that they should be generated from the same imaging data or with the same geometric parameters. Our imaging data provides us with a vector field and a `.stl` file, so we choose this as our starting point.

### FEBioStudio 2.10 workflow

1. File → New Model  →  Structural Mechanics
2. File → Import Geometry → choose `.stl` file
3. (Menu window at the right) → Build → Mesh
    -  Select the geometry by clicking directly on its representation
    - Mesh: The `.stl` file should appear under _Name_
    - Choose _Meshing Method_: TetGen / NetGen / Shell Mesh

    > TetGen: Generates "tet4" elements (or higher order tet elements). It requires a closed surface and returns errors otherwise. 
    > 
    > Example: For mesh dimensions of 6 x 6 x 14, an element size of 5 creates 1040 tet4 elements. For TA, size of 5 created 196956 elements.
    
4. File → Export FE model

### Fixing the `.stl` file

1. Install `MeshLab` (version 2020.09)
    ```
    sudo apt-get install meshlab
    ```
2. Open `Meshlab`. File → Import Mesh → choose `.stl` file
3. Check mesh: Filters → Quality Measures and Computations → Compute Geometric Measure
4. If _Mesh is not 'watertight'_, then: Filters → Remeshing, Simplification and Reconstruction → Surface Reconstruction: Screened Poisson
5. Delete original mesh
6. Save mesh: File → Export Mesh As
        