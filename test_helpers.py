import math

def generate_example_data():

    # create the terrain surface from N x N input data points (here simulated using
    # a simple function):
    N = 100
    coords = []  # x, y, z coordinates of all the points
    nodes = []  # tags of corresponding nodes
    tris = []  # connectivities (node tags) of triangle elements
    lin = [[], [], [], []]  # connectivities of boundary line elements


    def tag(i, j):
        return (N + 1) * i + j + 1


    for i in range(N + 1):
        for j in range(N + 1):
            nodes.append(tag(i, j))
            coords.extend([
                float(i) / N,
                float(j) / N, 0.05 * math.sin(10 * float(i + j) / N)
            ])
            if i > 0 and j > 0:
                tris.extend([tag(i - 1, j - 1), tag(i, j - 1), tag(i - 1, j)])
                tris.extend([tag(i, j - 1), tag(i, j), tag(i - 1, j)])
            if (i == 0 or i == N) and j > 0:
                lin[3 if i == 0 else 1].extend([tag(i, j - 1), tag(i, j)])
            if (j == 0 or j == N) and i > 0:
                lin[0 if j == 0 else 2].extend([tag(i - 1, j), tag(i, j)])
    pnt = [tag(0, 0), tag(N, 0), tag(N, N), tag(0, N)]  # corner points element

    return coords,nodes,tris,lin