import gmshterrain
from gmshterrain import _plot_gmsh_simple , _tag , terrain_to_gmsh , _read_csv_and_strip_header
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

# #Test Terrain to Gmsh with 10x10 Wave
# file = "./tests/test_data/test_gmshterrain/wave_10x10.csv"
# terrain_to_gmsh(file)

#Test Terrain to Gmsh with Resipy
file = "./tests/test_data/test_resipy/topography_resipy_no_heading.csv"
terrain_to_gmsh(file)

# print(tris)