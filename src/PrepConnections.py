from ConnectQuadToTet import save_to_obj
import sys

def vtkToObj(vtkMesh, filename):
    # get the vertices and faces from the vtk mesh.
    # obj is 1 indexed. vtk is 0 indexed.
    with open(vtkMesh, "r") as quadFile: 
        lines = quadFile.readlines()
        vertices = []
        faces = []
        numPoints = 0
        numCells = 0
        for line in lines:
            #startwith POINTS : vertices : x y z
            if numPoints > 0:
                vertices.append((line.split()))
                numPoints -= 1
            if line.startswith("POINTS"):
                numPoints = int(line.split()[1])     
            #startwith CELLS : Faces : 4 vertex vertex vertex vertex : the vertex is an index number, same as .obj
            if numCells > 0:
                nums = line.split()[1:]
                for i in range(len(nums)):
                    nums[i] = str(nums[i])
                faces.append(nums)
                numCells -= 1
            if line.startswith("CELLS"):
                numCells = int(line.split()[1])

    #write them to the obj, there is a function in SurfaceMesh.py or ConnectQuadToTet.py that does this.
    save_to_obj(filename, vertices, faces)
    return None

if "name" == "main":
    vtkMesh = sys.argv[1]
    outFile = sys.argv[2]
    vtkToObj(vtkMesh,outFile)
vtkToObj("quad.vtk", "convertedVTK.obj")

# Somehow calculate a boundary with which I can compare a point to in 
# order to determine if it is within the surface or not.
def findBoundary():
    # We have the boundary of the tet mesh, but we need to find the boundary of the quad mesh.

    # Go through each quad vertice until one is on the bounding curve.

    # use that one to include the rest. If bunding curve is preserved, then that should work.

    
    return None


# Pick a random point in the quad mesh, if in bounds, pass here to get the rest.
# This function will travel through halfedges to every vertice in the quad mesh, that is within the inp surface.
def breadthFirstSearch(boundaryLine: list):
    # Receive a starting point

    # BFS and find all the vertices along the boundary line.

    return None


def makeDictionaries(tetMesh, quadMesh):
    # make three dictionaries

    # 1. All vertices on the bottom
    # 2. All vertices on the side of the bottom
    # 3. All vertices on the rest of it

    return None

# assuming we only have a list of the vertex indices for the chunk
def findFaces(mesh, chunk):
    # Find the faces of the mesh.
    # Use the halfedge data structure to find all faces connected to the closest triangle vertex.
    # These are the indices of the faces adjacent to the closest triangle vertex.

    # turn mesh into a SurfaceMesh object.

    # make a set with all the vertex indices in the chunk.

    # initialize and empty faces set.


    # loop through each indice in chunk.
    # call surfacemesh.GetFacesAdjacentToVertex(vertexIndex) to get the faces adjacent to the vertex.
    # add faces not in the faces set to the faces set.
    # convert the vertex and face indices data to actual data from surfacemesh object.
    # use my saveToObj function to save the faces and vertices to an obj file.
    # return the filename or somehthing, its ready for ScaleUntrim.

    return None