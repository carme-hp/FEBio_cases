# Coupled fibers-mechanics simulation with preCICE

In this simulation we couple a `fiber` participant with a `mechanics` participant. This is a volume coupling example, where values are exchange accross the whole domain of both participants.

The coupling configuration is defined in the `precice-config.xml`. 

## The `fiber` participant
Only available in OpenDiHu. 
- [fibers-opendihu](fibers-opendihu)

## The `mechanics` participant
Available in OpenDiHu and FEBio
- [mechanics-opendihu](mechanics-opendihu)
- [mechanics-febio](mechanic-febio)