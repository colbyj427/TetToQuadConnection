# A python script meant to run the process of taking a tet mesh and creating a quad mesh of one of the boundaries.
# It also outputs a file containing the barycentric coordinates of the quad vertices in the tet mesh faces.
import sys
import subprocess
from pathlib import Path
import argparse
from TetToQuadConnection.src.ConnectQuadToTet import *
from TetToQuadConnection.src.PrepConnections import *

SCRIPT_DIR = Path(__file__).resolve().parent

def run_quadriflow_program(inputFile: str):
    """
    Runs the quadriflow program to create a quad mesh from a tet mesh input file.
    inputFile: str - Path to the tet mesh file.
    """
    projectRoot = Path(__file__).resolve().parent
    quadriflowExecutable = projectRoot / "build" / "quadriflow"

    if not quadriflowExecutable.exists():
        raise FileNotFoundError(f"C++ executable not found at {quadriflowExecutable}")
    
    
    command = [str(quadriflowExecutable), inputFile, "./output/quad.vtk", "TetToQuadConnection/build/setting.config"]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("OUTPUT:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"OUTPUT: {e.output}")
        print("END OF OUTPUT MESSAGE")
        print(f"ERROR OUTPUT: {e.stderr}")
        print("END OF ERROR MESSAGE")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# if __name__ == "__main__":
def runProcess(tetMesh: str, quadMesh: str = None):
    """
    A python script meant to run the process of taking a tet mesh and creating a quad mesh of one of the boundaries,
    then outputting a file connecting each vertex of both meshes by barycentric coordinates.
    "Usage: python main.py <tetMesh> <quadMesh>"
    tetMesh: str - Path to the tet mesh file.
    quadMesh: str - Path to the quad mesh file. If not provided, a quad mesh will be generated.
    """

    #if they provide a quad mesh, run code to connect meshes.
    if quadMesh is not None:
            connectQuadVertexOntoTriangle(tetMesh, quadMesh)
            print("Output stored in output/quadVertices.txt")
    #No quad mesh provided, run full program.
    else:
        # 3. Run the quadriflow algorithm to create a quad mesh from the boundary obj file.
        # this uses scale untrim / quadriflow
        run_quadriflow_program(tetMesh)
        # run_quadriflow_program(boundaryFilePath)
        vtkPath = Path("TetToQuadConnection/build/tempdir/quad.vtk")
        if not vtkPath.exists():
            raise FileNotFoundError("The generated quadrilateral vtk file does not exist.")

        # 4. Convert the vtk file to an obj file.
        quadMeshObjPath = Path("TetToQuadConnection/output/quadMeshBoundary.obj")
        vtkToObj(vtkPath, quadMeshObjPath)
        if not quadMeshObjPath.exists():
            raise FileNotFoundError("The converted quadrilateral obj file does not exist.")

        # 5. Run code to get the barycentric coordinates of quad vertices.
        connectQuadVertexOntoTriangle(tetMesh, str(quadMeshObjPath), "TetToQuadConnection/output/quadVertices.txt")
        # connectQuadVertexOntoTriangle(tetMesh, "./input/quadMeshBoundary.obj", "./output/quadVertices.txt")

        # print results
        print("Quad Mesh of the boundary file is stored at: input/quadMeshBoundary.obj")
        print("Barycentric information is stored in: output/quadVertices.txt")
