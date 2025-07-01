# A python script meant to run the process of taking a tet mesh and creating a quad mesh of one of the boundaries.
# It also outputs a file containing the barycentric coordinates of the quad vertices in the tet mesh faces.
import sys
import subprocess
from pathlib import Path
import argparse
from src.ConnectQuadToTet import *
from src.PrepConnections import *
# TODO : Move the file into the directory so I can import test_sweep_param directly.
# from test_sweep_param import meshHook

def run_quadriflow_program(inputFile: str):
    projectRoot = Path(__file__).resolve().parent
    quadriflowExecutable = projectRoot / "build" / "quadriflow"

    if not quadriflowExecutable.exists():
        raise FileNotFoundError(f"C++ executable not found at {quadriflowExecutable}")
     
    inputFilePath = "./input/" + inputFile
    command = [str(quadriflowExecutable), inputFilePath, "./output/quad.vtk", "build/setting.config"]

    try:
        print("Enter y to continue with quadriflow: ") # the program will ask for a check, I need to find a better way to do that.
                                                       # Im not sure if it needs to reach a certain point to enter y.
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Quadriflow output:\n", result.stdout) 
    except:
        print("Continuing with quadrilateral Mesh.", file=sys.stderr)    

if __name__ == "__main__":
    """
    "Usage: python main.py <tetMesh> <quadMesh>"
    """
    parser = argparse.ArgumentParser(description="Connect a quad mesh to a tet mesh.")

    parser.add_argument("tetMesh", type=str, help="Path to the tet mesh file.")
    parser.add_argument("quadMesh", nargs='?', default=None, type=str, help="Path to the quad mesh file. If not provided, a quad mesh will be generated.")

    args = parser.parse_args()

    tetMesh = args.tetMesh
    quadMesh = args.quadMesh

    #if they provide a quad mesh, run code to connect meshes.
    if quadMesh is not None:
            connectQuadVertexOntoTriangle(tetMesh, quadMesh)
            print("Output stored in output/quadVertices.txt")
    #No quad mesh provided, run full program.
    else:
        # TODO : Uncomment this section when it is implemented.
        # 1. First, create the boundary obj file from the tet mesh.
        # this uses Caleb's api
        # boundaryFilePath = Path("../input/tetBoundary.txt") # assuming the api returns a txt file
        # test_sweep_param.meshHook(tetMesh, boundaryFilePath)
        # if not boundaryFilePath.exists():
        #     raise FileNotFoundError("Could not find the generated boundary obj file.\n")

        # 2. Convert the txt boundary file into an obj file. 
        # This uses my code in PrepConnections.py
        # boundaryObjPath = Path("./input/inputTetMesh.obj")
        # convert_boundary_txt_to_obj(tetMesh, boundaryFilePath, boundaryObjPath)
        # if not boundaryObjPath.exists():
        #     raise FileNotFoundError("The converted boundary obj file does not exist.\n")

        # TODO : Uncomment variable path code when testing full functionality.
        # 3. Run the quadriflow algorithm to create a quad mesh from the boundary obj file.
        # this uses scale untrim / quadriflow
        run_quadriflow_program("inputTetMesh.obj")
        # run_quadriflow_program(boundaryFilePath)
        vtkPath = Path("./build/tempdir/quad.vtk")
        if not vtkPath.exists():
            raise FileNotFoundError("The generated quadrilateral vtk file does not exist.\n")

        # 4. Convert the vtk file to an obj file.
        quadMeshObjPath = Path("./input/quadMeshBoundary.obj")
        vtkToObj(vtkPath, quadMeshObjPath)
        if not quadMeshObjPath.exists():
            raise FileNotFoundError("The converted quadrilateral obj file does not exist.\n")

        # TODO : Uncomment variable path code when testing full functionality.
        # 5. Run code to get the barycentric coordinates of quad vertices.
        connectQuadVertexOntoTriangle("./input/inputTetMesh.obj", "./input/quadMeshBoundary.obj", "./output/quadVertices.txt")
        # connectQuadVertexOntoTriangle(tetMesh, "./input/quadMeshBoundary.obj", "./output/quadVertices.txt")

        # print results
        print("Tet mesh of the boundary is stored at: input/tetboundary.obj")
        print("Quad Mesh of the boundary file is stored at: input/quadMeshBoundary.obj")
        print("Barycentric information is stored in: output/quadVertices.txt")
