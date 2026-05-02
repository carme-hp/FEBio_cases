# Coupled fibers-mechanics of an ellipsoid muscle

## How to run

- The fiber participant (OpenDiHu)

```
mkorn && sr
cd build_release
./muscle_fibers ../fibers settings__muscle_fibers.py ramp.py
``` 

- The mechanics participant (0ption 1: OpenDiHu)

```
mkorn && sr
cd build_release
./muscle_contraction ../settings_muscle_mechanics.py ramp.py
``` 

- The mechanics participant (Option 2: OpenDiHu)

```
cd mechanics-febio
./run.sh biceps.feb
```

There are multiple input files available for FEBio, but they all describe the same geometry. 
`biceps.feb` has the finest mesh of all, while `biceps-coarse.feb` and `biceps-smooth.feb` have a similar resolution but in the second the mesh quality has been further improved. 



# Muscle geometry

The biceps geometry is based on imaging data of the Visible Human Male dataset (*V. Spitzer et al. “The Visible Human Male: A Technical Report”. In: J. Am. Med. Inf. Assoc. 3.2 (1996)*). 

The exact geometry files for the OpenDiHu participants are stored in the dataset [*Input data for OpenDiHu simulations*](https://doi.org/10.5281/zenodo.4705982), and information on the post-processing tecniques used for their creation can be found on the article *B. Maier and M. Schulte. “Mesh generation and multi-scale simulation of a contracting muscle–tendon complex”. In: J. Comput. Sci. Technol. 59 (2022)*.

For the FEBio simulation, we generated the mechanics mesh from the `.stl` file in the dataset and applied FEBioStudio 2.10's `tet4`. We used Blender to pre-process the `.stl` before applying FEBioStudio's meshing tool. 

Unlike the other cases, where the bottom end of the muscle (`z=0`) is fixed, here we apply the dirichlet boundary condition on the top level. 

## Mapping configuration

Todo

## FEBio simulations limitations

The FEbio simulation of the biceps does not converge already at the first timestep. This happens for all three tested meshes. The solution was to change the material parameters.

- material parameters designed to mimic OpenDiHu mechanics 

```
<material id="1" name="Material2" type="DiHuMaterial">
    <density>10</density>
    <k>1000</k>
    <pressure_model>default</pressure_model>
    <c1>3.176e-10</c1>
    <c2>1.813</c2>
    <c3>0</c3>
    <c4>1</c4>
    <c5>0.01075</c5>
    <lam_max>1</lam_max>
    <fiber type="vector">
        <vector>0,0,1</vector>
    </fiber>
    <active_contraction type="DiHuContraction">
        <pmax>7.3</pmax>
        <lam_opt>1.2</lam_opt>
        <enable_force_length_relation>1</enable_force_length_relation>
    </active_contraction>
</material>
```

- material parameters extracted from an febio-only contraction (see `biceps-smooth2.feb`)

```  
<material id="1" name="Material2" type="DiHuMaterial">
    <c1>13.85</c1>
    <c2>0.0</c2>
    <c3>2.07</c3>
    <c4>61.44</c4>
    <c5>640.7</c5>
    <k>100.0</k>
    <lam_max>1.03</lam_max>
    <fiber type="vector">0,0,1</fiber>
    <active_contraction type="DiHuContraction">
        <pmax>7.3</pmax>
        <lam_opt>1.2</lam_opt>
        <enable_force_length_relation>1</enable_force_length_relation>
    </active_contraction>
</material>
```