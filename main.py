import sys
import ConnectQuadToTet
import PrepConnections

def main(tetMesh, tetSurface, quadMesh=None):
    """
    Take in a tet mesh, tet mesh start surface, and an optional quad mesh,
    If no quad mesh is provided, create one with quadriflow.
    create the quad surface using boundary and breadth first search.
    superimpose the quad surface onto the tet surface.
    """
    return tetMesh, tetSurface, quadMesh

if "name" == "main":
    tetMesh = sys.argv[1]
    tetSurface = sys.argv[2]
    #fix this later to use an optional flag for giving their own quad mesh or not.
    quadMesh = sys.argv[3]

    #if quadriflow needs to be run, do it here.

    #open the files, passs in the descriptors, or whatever works in python.

    main(tetMesh, tetSurface, quadMesh)