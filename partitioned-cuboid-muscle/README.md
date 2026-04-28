# Coupled fibers-mechanics simulation of a cuboid muscle

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
./run.sh cuboid-muscle.feb
```

## Muscle geometry

A cuboid with size 3 x 3 x 12 cm. 

## Mapping configuration

Todo
