import gmshterrain
from gmshterrain import _tag , terrain_to_gmsh , _read_csv_and_strip_header
import test_helpers

#print(gmshterrain._read_csv_and_strip_header("./tests/test_data/test_csv/with_header.csv"))

# coords,nodes,tris,lin = test_helpers.generate_example_data()
# gmshterrain.terrain_to_gmsh(coords,nodes,tris,lin)

#coords,nodes,tris,lin = gmshterrain.link_coordinates("./tests/test_data/test_csv/with_header.csv")
# file = "./tests/test_data/test_resipy/topography_resipy_no_heading.csv"
# print(_read_csv_and_strip_header(file))

# coords = []

# N,M=10,10

# nodes,tris,lin,pnt = gmshterrain._create_nodes_and_connectivities(coords,N,M)
# print(tris)

file = "./tests/test_data/test_gmshterrain/wave_10x10.csv"
nodes,tris,lin,pnt = terrain_to_gmsh(file)

print(tris)