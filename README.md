# gmshterrain
## Overview
gmshterrain is a series of Python utilities designed to produce a gmsh surface from gridded terrain data.
## Inputs
Terrain data must be gridded, by which we mean:
1. The data must be organised into x, y and z columns.
2. The data must treat x as an inner loop and y as an outer loop
3. The data must be "square"
4. Each interval must be in equal steps
5. There must be no gaps
