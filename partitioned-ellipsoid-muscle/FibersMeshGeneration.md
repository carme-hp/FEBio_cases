# Fiber Mesh Generation

The fibers mesh is defined via a `.json` file, which requires changes in `variables/variables.py` and in `settings_fibers.py`.

The `.json` file should have the following structure:
```JSON
{
  "fiber0": [{"x":..., "y":..., "z":...}, ...],
  "fiber1": [{"x":..., "y":..., "z":...}, ...]
}
```

If you want to create fiber meshes for dummy ellipsoid muscles, we refer you to use [our pipeline](https://github.com/carme-hp/muscle_prestretch_dataset/tree/main).

The creation of `.json` files from imaging data is supported via [BioMesh](https://github.com/opendihu/biomesh).

**Helper Scripts**

- The script `check_fiber_mesh.py` is provided so you can visualize the fiber mesh in ParaView without having to run the simulation. For that, you will need to use the `Filters → Tube`.


    ```
    python check_fiber_mesh.py fiber_file_name.json 
    ```

- The script `count_fibers_points.py` can be run to quickly find out the number of fibers and their number of points. 
    ```
    python count_fibers_points.py fiber_file_name.json 
    ```