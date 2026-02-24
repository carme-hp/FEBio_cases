# Simulating muscle contraction with FEBio

This repository provides simulation examples for the [FEBio adapter](https://github.com/carme-hp/FEBio_adapter/tree/main), an adapter to couple FEBio and [OpenDiHu](https://github.com/opendihu/opendihu) via preCICE to run simulations of skeletal muscles.

### Structure

- [partitioned-muscle-contraction](partitioned-muscle-contraction): Provides the input files and instructions to run a coupled fibers-mechanics simulation with preCICE.

- [monolithic-muscle-contraction](monolithic-muscle-contraction): Provides the input files and instructions to run a monolithic fibers-mechanics simulation using OpenDiHu. This is meant to be used for comparison purposes.

- [monolithic-muscle-elongation](monolithic-muscle-elongation): Provides the input files and instructions to run a mechanics simulation with OpenDiHu and FEBio. It involves no coupling, but it might be useful for comparison. 

