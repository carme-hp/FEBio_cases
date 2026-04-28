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

Todo
