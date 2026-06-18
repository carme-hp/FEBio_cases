# Simulating muscle contraction with FEBio

This repository provides simulation examples for the [FEBio adapter](https://github.com/carme-hp/FEBio_adapter/tree/main), an adapter to couple FEBio and [OpenDiHu](https://github.com/opendihu/opendihu) via preCICE to run simulations of skeletal muscles.

## List of partitioned cases

We simulate muscle contraction using a partitioned approach. We couple the electrophysiology (fibers participant) to the mechanics (muscle participant). The fiber participant is only available in OpenDiHu while the muscle participant is available both in OpenDiHu and in FEBio. We test our approach on multiple scenarios, all of them consisting of a muscle that contracts along the z-axis. One of the muscle ends (z=0) is fixed while the other is free to move.


- [partitioned-cuboid-muscle](partitioned-cuboid-muscle): Contraction of a cuboid muscle. Geometry is manually defined in OpenDiHu. Mechanics are implemented in OpenDiHu and in FEBio (both structured grid). 

- [partitioned-fusiform-muscle](partitioned-fusiform-muscle): Contraction of an fusiform muscle. Geometry is created using https://github.com/carme-hp/muscle_prestretch_dataset/tree/main (fibers are read from a .json file).

- [partitioned-biceps](partitioned-biceps): Contraction of the biceps. Geometry is read from OpenDiHu hard-coded files created by Benjamin Maier. Mechanics are implemented in OpenDiHu (structured grid) and in FEBio (unstructured grid).

- [partitioned-tibialis-anterior](partitioned-tibialis-anterior): Contraction of the tibialis-anterior. Mechanics only in FEBio (structured grid not available).


## List of monolithic cases

Mainly added here for validation purposes.

- [monolithic-muscle-contraction](monolithic-muscle-contraction): Provides the input files and instructions to run a monolithic fibers-mechanics simulation using OpenDiHu. This is meant to be used for comparison purposes.

- [monolithic-muscle-elongation](monolithic-muscle-elongation): Provides the input files and instructions to run a mechanics simulation with OpenDiHu and FEBio. It involves no coupling, but it might be useful for comparison. 

## How to run an OpenDiHu simulation

Install OpenDiHu and define `$OPENDIHU_HOME` and aliases `mkorn='$OPENDIHU_HOME/scripts/shortcuts/mkorn.sh'` and `sr='$OPENDIHU_HOME/scripts/shortcuts/sr.sh'`. Now you can build the simulation case on release mode with `mkorn && sr`. 

Typically, partitioned cases contain a `fibers-opendihu` and a ``mechanics-opendihu`. To build and run these cases you need to run

```
cd fibers-opendihu
mkorn && sr
./build_release/fibers settings_fibers.py
``` 
and

```
cd mechanics-opendihu
mkorn && sr
./build_release/muscle settings_muscle.py
``` 

respectively.

## How to run a FEBio simulation

Install FEBio and the FEBio adapter. See [https://github.com/carme-hp/FEBio_adapter/tree/main/bfp_plugin](instructions).

How to run:
```
cd mechanics-febio
./run.sh muscle.feb
```
