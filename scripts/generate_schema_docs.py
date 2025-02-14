#!/usr/bin/env python3

import json2asciidoc

# Generate asciidoc files for all JSON schemas in the content folder structure

# Geometry

json2asciidoc.generate_asciidoc_file("../schemas/asset_schema.json", "../content/07_geometry/")
json2asciidoc.generate_asciidoc_file("../schemas/mapping_schema.json", "../content/07_geometry/")

# Material

json2asciidoc.generate_asciidoc_file("../schemas/material_schema.json", "../content/08_material/")
json2asciidoc.generate_asciidoc_file("../schemas/material_emp_schema.json", "../content/08_material/")
json2asciidoc.generate_asciidoc_file("../schemas/material_optical_schema.json", "../content/08_material/")
json2asciidoc.generate_asciidoc_file("../schemas/material_brdf_schema.json", "../content/08_material/")
json2asciidoc.generate_asciidoc_file("../schemas/material_reflectance_schema.json", "../content/08_material/")