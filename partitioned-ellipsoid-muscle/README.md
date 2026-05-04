# Coupled fibers-mechanics of an ellipsoid muscle

## How to run

- The fiber participant (OpenDiHu)

```
cd fibers-opendihu
mkorn && sr
./build_release/fibers settings_fibers.py
``` 

- The mechanics participant (0ption 1: OpenDiHu)

```
cd mechanics-opendihu
mkorn && sr
./build_release/muscle settings_muscle.py
``` 

- The mechanics participant (Option 2: OpenDiHu)

```
cd mechanics-febio
./run.sh ellipsoid-muscle.feb
```

# Muscle geometry

The geometry is an ellipsoid like muscle with length 14 cm and a radius of 3cm at the center. 

The geometry is defined by

- `fibers_1.json` 
- `3D_mesh_1.vtk`


These geometry files were was generated using the geometry generation pipeline available on [our repository](https://github.com/carme-hp/muscle_prestretch_dataset/tree/main). To reproduce, use the following parameters:

```
id = 1
n_fibers = 40
nx = 5
ny = 5
nz = 21
L = 14
Rmax = 3
Rmin = 2
```

To parse the `3D_mesh_1.vtk` the script `read_structured_vtk.py` from our repository is provided.

## Mapping configuration

- **From Muscle to fibers**

`nearest-neighbor` mapping does not work to transfer the geometry: since the geometry mesh is coarser, applying the geometry into the fibers mesh results into clustering the fiber points at the locations of the  points in the mechanics mesh.

This can be easily checked by comparing the precice exports to the fiber solver output files (number of points is the same, but the points in the fiber solver overlap). In practice, the fiber simulation goes through, but no contraction is observed and the solution vector in the Fibers contains nans.

|  | **geometry (from muscle to fibers)** | **gamma (from fibers to muscle)** | Observations |
| --- | --- | --- | --- |
| **results1** | rbf (100, 0.2, 3) | rbf (100, 0.2, 3) |  |
| **results2** | rbf (default, 3) | rbf (default, 3) |  |
| **results3** | nearest-neighbour | nearest-neighbour | no contraction, fiber mesh looks wrong |
| **results4** | nearest-neighbour | rbf (default, 3) | no contraction, fiber mesh looks wrong |
| **results5** |  rbf (default, 3) |nearest-neighbour |  |
| **results6** | nearest-neighbour, no initialization | nearest-neighbour | no contraction, fiber mesh looks wrong |


![alt text](pics/broken_mapping.png)

