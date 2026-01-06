import gmshterrain
import test_helpers



coords,nodes,tris,lin = test_helpers.generate_example_data()
gmshterrain.terrain_to_gmsh(coords,nodes,tris,lin)