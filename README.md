# Simulating muscle contraction with FEBio

This repository provides simulation examples for the [FEBio adapter](https://github.com/carme-hp/FEBio_adapter/tree/main), an adapter to couple FEBio and [OpenDiHu](https://github.com/opendihu/opendihu) via preCICE to run simulations of skeletal muscles.

## List of partitioned cases

Coupled simulations for muscle contractions.

- [partitioned-biceps](partitioned-biceps): Contraction of the biceps. Geometry is read from OpenDiHu hard-coded files created by Benjamin Maier. Mechanics are implemented in OpenDiHu (structured grid) and in FEBio (unstructured grid).

- [partitioned-cuboid-muscle](partitioned-cuboid-muscle): Contraction of a cuboid muscle. Geometry is manually defined in OpenDiHu. Mechanics are implemented in OpenDiHu and in FEBio (both structured grid). 

- [partioned-ellipsoid-muscle](partitioned-ellipsoid-muscle): Contraction of a cuboid muscle. Geometry is created using https://github.com/carme-hp/muscle_prestretch_dataset/tree/main.

## List of monolithic cases

Mainly added here for validation purposes.

- [monolithic-muscle-contraction](monolithic-muscle-contraction): Provides the input files and instructions to run a monolithic fibers-mechanics simulation using OpenDiHu. This is meant to be used for comparison purposes.

- [monolithic-muscle-elongation](monolithic-muscle-elongation): Provides the input files and instructions to run a mechanics simulation with OpenDiHu and FEBio. It involves no coupling, but it might be useful for comparison. 


