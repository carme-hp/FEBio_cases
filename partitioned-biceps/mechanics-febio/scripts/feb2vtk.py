import xml.etree.ElementTree as ET
import numpy as np
import meshio

tree = ET.parse("../biceps-smooth.feb") # path to your FEBio file
root = tree.getroot()

# --- Extract nodes ---
nodes = []
for node in root.findall(".//Nodes/node"):
    coords = list(map(float, node.text.strip().split(',')))
    nodes.append(coords)

points = np.array(nodes)

# --- Extract elements ---
cells = []
cell_types = []

for elem_block in root.findall(".//Elements"):
    etype = elem_block.attrib.get("type")

    connectivity = []
    for elem in elem_block.findall("elem"):
        conn = list(map(int, elem.text.strip().split(',')))
        connectivity.append([i - 1 for i in conn])  # FEBio is 1-based

    if etype in ["tet4"]:
        cells.append(("tetra", np.array(connectivity)))
    elif etype in ["hex8"]:
        cells.append(("hexahedron", np.array(connectivity)))
    elif etype in ["tri3"]:
        cells.append(("triangle", np.array(connectivity)))
    elif etype in ["quad4"]:
        cells.append(("quad", np.array(connectivity)))
    else:
        print(f"Unsupported element type: {etype}")

# --- Write VTK ---
mesh = meshio.Mesh(points=points, cells=cells)
mesh.write("output.vtk")

print("Converted to output.vtk")