# Coupled fibers-mechanics simulation with preCICE

In this simulation we couple a `fiber` participant with a `mechanics` participant. This is a volume coupling example, where values are exchange accross the whole domain of both participants.

The coupling configuration is defined in the `precice-config.xml`. 

## The `fiber` participant
Only available in OpenDiHu. 
- [fibers-opendihu](fibers-opendihu)

How to build and run: 
```
cd fibers-opendihu
mkorn && sr
cd build_release
./build_release/fibers settings_fibers.py
``` 

## The `mechanics` participant
Available in OpenDiHu and FEBio
- [mechanics-opendihu](mechanics-opendihu)

How to build and run: 
```
cd mechanics-opendihu
mkorn && sr
cd build_release
./build_release/muscle settings_muscle.py
``` 

- [mechanics-febio](mechanic-febio)

How to run:
```
cd mechanics-febio
BFP_CONFIG="../precice-config.xml" ./run.sh muscle.feb
```