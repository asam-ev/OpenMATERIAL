# Examples

This folder contains examples for all file formats defined in {THIS_STANDARD}.
This showcases the usage of asset files alongside a 3D model file, the material assignment via mesh or texture, the mapping to material property files als well as the definition of specific property look-up tables.

| File Name                            | Description                                                                                                                                 |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| `checker.png`                        | Visual texture used in the 3D model.                                                                                                        |
| `checker_xom.png`                    | {THIS_STANDARD} assignment texture used to assign different materials to certain parts of the object (texture-based material assignment).   |
| `example_asset.gltf/bin`             | 3D model file in glTF format, representing the 3D geometry.                                                                                 |
| `example_asset.xoma`                 | {THIS_STANDARD} asset file (.xoma), containing asset metadata and the link to the assignment texture.                                       |
| `example_mapping.xomm`               | Material mapping file (.xomm), providing mappings for different material definitions, per mesh or texture color value.                      |
| `example_material.xomp`              | {THIS_STANDARD} material property file (.xomp), defining core material characteristics.                                                     |
| `example_material_2.xomp`            | Second example of an {THIS_STANDARD} material property file to showcase the mapping of multiple materials.                                  |
| `example_material_emp.xompt`         | Material property look-up table (.xompt), containing electromagnetic properties.                                                            |
| `example_material_camera_brdf.xompt` | Material property look-up table (.xompt), containing BRDF data specific to camera sensors.                                                  |
| `example_material_lidar_brdf.xompt`  | Material property look-up table (.xompt), containing BRDF data specific to lidar sensors.                                                   |
| `example_material_radar_brdf.xompt`  | Material property look-up table (.xompt), containing BRDF data specific to radar sensors.                                                   |
