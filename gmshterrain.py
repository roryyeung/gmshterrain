import gmsh
import math
import sys
import csv

def terrain_to_gmsh(file):
    """
    Wrapper function that calls the required functions in order.
    """

    # Storage for the expected outputs
    coords = _read_csv_and_strip_header(file)  # x, y, z coordinates of all the points

    #This helper function checks data is correctly gridded, and if so, returns summary statistics
    #(Note that N & M are the number of nodes in the X and Y directions)
    x_max,x_min,y_max,y_min,N,M = _check_data_is_gridded_and_return_summaries(coords)
    corners = {"x_max":x_max,"x_min":x_min,"y_max":y_max,"y_min":y_min}

    #This helper function creates the nodes, tris and lin, from a given set of correctly gridded coords
    nodes,tris,lin,pnt = _create_nodes_and_connectivities(coords,N,M)
    
    print(f"Length of nodes: {len(nodes)}")
    print(f"Length of coords: {len(coords)}")


    #TODO - Describe Boundary Line Elements

    # #TODO - Implament Plotting Fuction
    # #Call the Function to do the GMSH plotting
    # _plot_gmsh(coords,nodes,tris,lin,pnt,N,M)

    _plot_gmsh_simple(coords,nodes,tris,lin,pnt,N,M,corners)

def _plot_gmsh(coords,nodes,tris,lin,pnt,N,M):
    """
    This function accepts a set of 3D datapoints in a regular grid and plots them in Gmsh.

    Note that this requires a regular xy grid of topography data - if you don't have this,
    you many need to use another function to infer this.

    Inputs

    coords  x, y, z coordinates of all the points
    nodes   tags of corresponding nodes
    tris    connectivities (node tags) of triangle elements
    lin     connectivities of boundary line elements

    Returns

    No Return - creates popup via Gmsh.
    """

    gmsh.initialize(sys.argv)

    gmsh.model.add("terrain")

    # create 4 corner points
    #TODO - modify these to the general case
    gmsh.model.geo.addPoint(0, 0, coords[3 * _tag(0, 0, N) - 1], 1)
    gmsh.model.geo.addPoint(1, 0, coords[3 * _tag(N, 0, N) - 1], 2)
    gmsh.model.geo.addPoint(1, 1, coords[3 * _tag(N, N, N) - 1], 3)
    gmsh.model.geo.addPoint(0, 1, coords[3 * _tag(0, N, N) - 1], 4)
    gmsh.model.geo.synchronize()

    # create 4 discrete bounding curves, with their boundary points
    
    for i in range(4):
        gmsh.model.addDiscreteEntity(1, i + 1, [i + 1, i + 2 if i < 3 else 1])

    # create one discrete surface, with its bounding curves
    gmsh.model.addDiscreteEntity(2, 1, [1, 2, -3, -4])

    # add all the nodes on the surface (for simplicity... see below)
    gmsh.model.mesh.addNodes(2, 1, nodes, coords)

    # add elements on the 4 points, the 4 curves and the surface
    for i in range(4):
        # type 15 for point elements:
        gmsh.model.mesh.addElementsByType(i + 1, 15, [], [pnt[i]])
        # type 1 for 2-node line elements:
        gmsh.model.mesh.addElementsByType(i + 1, 1, [], lin[i])
    # type 2 for 3-node triangle elements:
    gmsh.model.mesh.addElementsByType(1, 2, [], tris)

    # reclassify the nodes on the curves and the points (since we put them all on
    # the surface before for simplicity)
    gmsh.model.mesh.reclassifyNodes()

    # note that for more complicated meshes, e.g. for on input unstructured STL, we
    # could use gmsh.model.mesh.classifySurfaces() to automatically create the
    # discrete entities and the topology; but we would have to extract the
    # boundaries afterwards

    # create a geometry for the discrete curves and surfaces, so that we can remesh
    # them
    gmsh.model.mesh.createGeometry()


    #TODO - Modify the below blocks to only create a volume below the surface?

    # create other CAD entities to form one volume below the terrain surface, and
    # one volume on top; beware that only built-in CAD entities can be hybrid,
    # i.e. have discrete entities on their boundary: OpenCASCADE does not support
    # this feature
    # p1 = gmsh.model.geo.addPoint(0, 0, -0.5)
    # p2 = gmsh.model.geo.addPoint(1, 0, -0.5)
    # p3 = gmsh.model.geo.addPoint(1, 1, -0.5)
    # p4 = gmsh.model.geo.addPoint(0, 1, -0.5)
    # p5 = gmsh.model.geo.addPoint(0, 0, 0.5)
    # p6 = gmsh.model.geo.addPoint(1, 0, 0.5)
    # p7 = gmsh.model.geo.addPoint(1, 1, 0.5)
    # p8 = gmsh.model.geo.addPoint(0, 1, 0.5)

    # c1 = gmsh.model.geo.addLine(p1, p2)
    # c2 = gmsh.model.geo.addLine(p2, p3)
    # c3 = gmsh.model.geo.addLine(p3, p4)
    # c4 = gmsh.model.geo.addLine(p4, p1)

    # c5 = gmsh.model.geo.addLine(p5, p6)
    # c6 = gmsh.model.geo.addLine(p6, p7)
    # c7 = gmsh.model.geo.addLine(p7, p8)
    # c8 = gmsh.model.geo.addLine(p8, p5)

    # c10 = gmsh.model.geo.addLine(p1, 1)
    # c11 = gmsh.model.geo.addLine(p2, 2)
    # c12 = gmsh.model.geo.addLine(p3, 3)
    # c13 = gmsh.model.geo.addLine(p4, 4)

    # c14 = gmsh.model.geo.addLine(1, p5)
    # c15 = gmsh.model.geo.addLine(2, p6)
    # c16 = gmsh.model.geo.addLine(3, p7)
    # c17 = gmsh.model.geo.addLine(4, p8)

    # # bottom and top
    # ll1 = gmsh.model.geo.addCurveLoop([c1, c2, c3, c4])
    # s1 = gmsh.model.geo.addPlaneSurface([ll1])
    # ll2 = gmsh.model.geo.addCurveLoop([c5, c6, c7, c8])
    # s2 = gmsh.model.geo.addPlaneSurface([ll2])

    # # lower
    # ll3 = gmsh.model.geo.addCurveLoop([c1, c11, -1, -c10])
    # s3 = gmsh.model.geo.addPlaneSurface([ll3])
    # ll4 = gmsh.model.geo.addCurveLoop([c2, c12, -2, -c11])
    # s4 = gmsh.model.geo.addPlaneSurface([ll4])
    # ll5 = gmsh.model.geo.addCurveLoop([c3, c13, 3, -c12])
    # s5 = gmsh.model.geo.addPlaneSurface([ll5])
    # ll6 = gmsh.model.geo.addCurveLoop([c4, c10, 4, -c13])
    # s6 = gmsh.model.geo.addPlaneSurface([ll6])
    # sl1 = gmsh.model.geo.addSurfaceLoop([s1, s3, s4, s5, s6, 1])
    # v1 = gmsh.model.geo.addVolume([sl1])

    # # upper
    # ll7 = gmsh.model.geo.addCurveLoop([c5, -c15, -1, c14])
    # s7 = gmsh.model.geo.addPlaneSurface([ll7])
    # ll8 = gmsh.model.geo.addCurveLoop([c6, -c16, -2, c15])
    # s8 = gmsh.model.geo.addPlaneSurface([ll8])
    # ll9 = gmsh.model.geo.addCurveLoop([c7, -c17, 3, c16])
    # s9 = gmsh.model.geo.addPlaneSurface([ll9])
    # ll10 = gmsh.model.geo.addCurveLoop([c8, -c14, 4, c17])
    # s10 = gmsh.model.geo.addPlaneSurface([ll10])
    # sl2 = gmsh.model.geo.addSurfaceLoop([s2, s7, s8, s9, s10, 1])
    # v2 = gmsh.model.geo.addVolume([sl2])

    gmsh.model.geo.synchronize()

    # set this to True to build a fully hex mesh
    #transfinite = True
    transfinite = False

    if transfinite:
        NN = 30
        for c in gmsh.model.getEntities(1):
            gmsh.model.mesh.setTransfiniteCurve(c[1], NN)
        for s in gmsh.model.getEntities(2):
            gmsh.model.mesh.setTransfiniteSurface(s[1])
            gmsh.model.mesh.setRecombine(s[0], s[1])
            gmsh.model.mesh.setSmoothing(s[0], s[1], 100)
        gmsh.model.mesh.setTransfiniteVolume(v1)
        gmsh.model.mesh.setTransfiniteVolume(v2)
    else:
        gmsh.option.setNumber('Mesh.MeshSizeMin', 0.05)
        gmsh.option.setNumber('Mesh.MeshSizeMax', 0.05)

    #TODO - Consider how to pass this data out
    #TODO - Consider how to add the surrounding volumes / boxes?

    #gmsh.model.mesh.generate(2)
    #gmsh.write('terrain.msh')

    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

    gmsh.finalize()

def _plot_gmsh_simple(coords,nodes,tris,lin,pnt,N,M,corners):
    
    gmsh.initialize(sys.argv)
    gmsh.model.add("terrain")

    # Unpack the four corners
    x_max = corners["x_max"]
    x_min = corners["x_min"] 
    y_max = corners["y_max"]
    y_min = corners["y_min"]

    # create 4 corner points to "contain surface 1"
    lc = 1e-2
    Num_Nodes = N * M 
    #TODO - Look Up the y-coordinates!
    #TODO - calculate the correct lc
    Corner_node_1 = Num_Nodes + 1
    Corner_node_2 = Num_Nodes + 2
    Corner_node_3 = Num_Nodes + 3
    Corner_node_4 = Num_Nodes + 4

    gmsh.model.geo.addPoint(x_min,y_min,0,lc,Corner_node_1)
    gmsh.model.geo.addPoint(x_max,y_min,0,lc,Corner_node_2)
    gmsh.model.geo.addPoint(x_max,y_max,0,lc,Corner_node_3)
    gmsh.model.geo.addPoint(x_min,y_max,0,lc,Corner_node_4)
    gmsh.model.geo.synchronize()

    # Create the bounding curves using these boundary points
    gmsh.model.addDiscreteEntity(1,1,[Corner_node_1,Corner_node_2])
    gmsh.model.addDiscreteEntity(1,2,[Corner_node_2,Corner_node_3])
    gmsh.model.addDiscreteEntity(1,3,[Corner_node_3,Corner_node_4])
    gmsh.model.addDiscreteEntity(1,4,[Corner_node_4,Corner_node_1])
    gmsh.model.geo.synchronize()

    # create one discrete surface, with its bounding curves
    gmsh.model.addDiscreteEntity(2, 1, [1, 2, 3,4])
    gmsh.model.geo.synchronize()

    #Add all the nodes to "Surface 1"
    gmsh.model.mesh.addNodes(2, 1, nodes, coords)

    #TODO - Implement Rest of this Section
    # add elements on the 4 points, the 4 curves and the surface
    # for i in range(4):
    #     # type 15 for point elements:
    #     gmsh.model.mesh.addElementsByType(i + 1, 15, [], [pnt[i]])
    #     # type 1 for 2-node line elements:
    #     gmsh.model.mesh.addElementsByType(i + 1, 1, [], lin[i])
    # type 2 for 3-node triangle elements:
    gmsh.model.mesh.addElementsByType(1, 2, [], tris)

    #Export This to Gmsh
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()

    gmsh.finalize()

def _read_csv_and_strip_header(file):
    """
    Docstring for _read_csv_and_strip_header
    
    Input: file - location of the csv file
    Output: coords - a list of lists
    """
    coords = []
    with open(file,"r") as csvfile:
        csvreader = csv.reader(csvfile,delimiter="," , quoting=csv.QUOTE_NONNUMERIC)
        header = next(csvreader)
        #Check if no header - if so append to coords list
        if (
            (isinstance(header[0],float)) and
            (isinstance(header[1],float)) and
            (isinstance(header[2],float))
        ):
            coords.extend(header)
        for row in csvreader:
            coords.extend(row)
    return coords

def _check_data_is_gridded_and_return_summaries(coords):
    """
    Helper function to check if coords are correctly gridded & sorted and raise exeption
    if not. Data should be sorted by y (outer loop) then x(inner loop).

    If correctly gridded, returns min and max of both x and y coodinates.
    """

    #Unpack and summerise coords
    x_values = []
    for i, item in enumerate(coords):
        if i % 3 == 0:
            x_values.append(item)
    x_max = max(x_values)
    x_min = min(x_values)
    N = len(set(x_values))
    y_values = []
    for i, item in enumerate(coords):
        if i % 3 == 1:
            y_values.append(item)
    y_max = max(y_values)
    y_min = min(y_values)
    M = len(set(y_values))

    #TODO - Write helper function to identify if the data is correctly gridded & sorted

    #Return summeries
    return x_max,x_min,y_max,y_min,N,M

def _tag(i, j,N):
    """Creates unique tags for each node, as required by Gmsh"""
    return (N + 1) * i + j + 1

def _create_nodes_and_connectivities(coords,N,M):
    """
    This helper function accepts a set of properly gridded cords and constructs the geometry for gmsh.
    #TODO - Write remaining documentation
    #TODO - Implement Function
    """

    #This block recreates the required formats, independently of external function
    nodes = []  # tags of corresponding nodes
    tris = []  # connectivities (node tags) of triangle elements
    lin = [[], [], [], []]  # connectivities of boundary line elements

    #TODO - Modify example code below
    #This block creates nodes and connectivities for each coordinate 
    for i in range(N): #why N+1?
        for j in range(M): # Updated from N to M
            #This section creates the tag for each node
            nodes.append(_tag(i, j,N))
            #This section creates the geometry
            if i > 0 and j > 0:
                tris.extend([_tag(i - 1, j - 1,N), _tag(i, j - 1,N), _tag(i - 1, j,N)])
                tris.extend([_tag(i, j - 1,N), _tag(i, j,N), _tag(i - 1, j,N)])
            if (i == 0 or i == N) and j > 0:
                lin[3 if i == 0 else 1].extend([_tag(i, j - 1,N), _tag(i, j,N)])
            if (j == 0 or j == N) and i > 0:
                lin[0 if j == 0 else 2].extend([_tag(i - 1, j,N), _tag(i, j,N)])
    #This section creates the corner points element
    pnt = [_tag(0, 0, N), _tag(N, 0, N), _tag(N, N, N), _tag(0, N, N)]  # corner points element

    return nodes,tris,lin,pnt