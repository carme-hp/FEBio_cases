# Coupled fibers-mechanics simulation with preCICE

In this simulation we couple a `fiber` participant with a `mechanics` participant. This is a volume coupling example, where values are exchange accross the whole domain of both participants.

The coupling configuration is defined in the `precice-config.xml`. 

## The `fiber` participant
Only available in OpenDiHu. 
- [fibers-opendihu](fibers-opendihu)

Install OpenDiHu and define `$OPENDIHU_HOME` and aliases `mkorn='$OPENDIHU_HOME/scripts/shortcuts/mkorn.sh'` and `sr='$OPENDIHU_HOME/scripts/shortcuts/sr.sh'`. Then you can build and run as follows:

```
cd fibers-opendihu
mkorn && sr
./build_release/fibers settings_fibers.py
``` 

## The `mechanics` participant
Available in OpenDiHu and FEBio
- [mechanics-opendihu](mechanics-opendihu)

Install OpenDiHu and define `$OPENDIHU_HOME` and aliases `mkorn='$OPENDIHU_HOME/scripts/shortcuts/mkorn.sh'` and `sr='$OPENDIHU_HOME/scripts/shortcuts/sr.sh'`. Then you can build and run as follows:

```
cd mechanics-opendihu
mkorn && sr
./build_release/muscle settings_muscle.py
``` 

- [mechanics-febio](mechanic-febio)

Install FEBio and the FEBio adapter. See [https://github.com/carme-hp/FEBio_adapter/tree/main/bfp_plugin](instructions).

How to run:
```
cd mechanics-febio
./run.sh muscle.feb
```

# Mesh Generation

To run a successful simulation for a given geometry, you have to generate the corresonding mesh files that satisfy the input requirements. 

- The **fiber mesh** for OpenDiHu is encoded in a `.json` file. Refer to the [instructions for generation of fiber mesh](FibersMeshGeneration) to create your own mesh files or to visualize the provided `.json` files.

- The requirements on the **mechanics mesh** are different depending on the solver of choice, e.g., OpenDiHu or FEBio. To learn more about the requirements and how to generate mechanics meshes, refer to the [instructions for generation of mechanics mesh](MechanicsMeshGeneration). 

