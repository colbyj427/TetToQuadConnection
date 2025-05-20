from numpy import *
import builtins  # For explicit use of Python's built-in min and max
from surfacemesh import SurfaceMesh



def project_point_onto_triangle_plane(point, v0, v1, v2):
    """
    Projects a 3D point onto a triangular face defined by vertices v0, v1, v2.
    
    Args:
        point (np.array): The 3D point to project (x, y, z).
        v0, v1, v2 (np.array): The vertices of the triangle (x, y, z).
        
    Returns:
        np.array: The projected point on the plane of the triangle.
    """
    # Convert to numpy arrays
    point = array(point)
    v0, v1, v2 = array(v0), array(v1), array(v2)
    
    # Calculate plane normal
    normal = cross(v1 - v0, v2 - v0)
    normal = normal / linalg.norm(normal)
    
    # Find the projection of the point onto the plane
    point_to_v0 = point - v0
    distance_to_plane = dot(point_to_v0, normal)
    projected_point = point - distance_to_plane * normal

    return  projected_point

def project_point_onto_triangle_edge(point, v0, v1):
    """
    Projects a 3D point onto an edge defined by vertices v0, v1.
    
    Args:
        point (np.array): The 3D point to project (x, y, z).
        v0, v1 (np.array): The vertices of the edge (x, y, z).
        
    Returns:
        np.array: The projected point on the edge.
    """
    # Convert to numpy arrays
    point = array(point)
    v0, v1 = array(v0), array(v1)
    
    # Calculate edge vector
    edge = v1 - v0
    edge_length = linalg.norm(edge)
    edge = edge / edge_length  # Normalize edge vector
    
    # Find the projection of the point onto the edge
    point_to_v0 = point - v0
    distance_to_edge = dot(point_to_v0, edge)

    distance_to_edge_float = float(distance_to_edge)
    edge_length_float = float(edge_length)

    # Clamp the projection distance to ensure it's within the edge segment
    distance_to_edge = builtins.max(0, builtins.min(distance_to_edge_float, edge_length_float)) # throwing type error

    projected_point = v0 + distance_to_edge * edge

    # Now we need to return the closest point on the edge itself, along with the distance from the point we started with.
    distance = linalg.norm(point - projected_point)

    return  projected_point , distance


def convertToBarycentric(p, a, b, c):
    '''
    Compute barycentric coordinates (u, v, w) for
    point p with respect to triangle (a, b, c)
    '''

    v0 = b - a
    v1 = c - a
    v2 = p - a
    d00 = dot(v0, v0)
    d01 = dot(v0, v1)
    d11 = dot(v1, v1)
    d20 = dot(v2, v0)
    d21 = dot(v2, v1)
    denom = d00 * d11 - d01 * d01
    v = (d11 * d20 - d01 * d21) / denom
    w = (d00 * d21 - d01 * d20) / denom
    u = 1.0 - v - w
    return array([u, v, w])

def save_to_obj(file_path, vertices, faces):
    """
    Saves vertices and faces to a .obj file.

    Args:
        file_path (str): The output file path.
        vertices (np.array): A (N, 3) array of vertex positions (x, y, z).
        faces (np.array): A (M, 3) or (M, 4) array of faces (vertex indices, 1-based).
    """
    with open(file_path, 'w') as obj_file:
        # Write vertices
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        
        # Write faces
        for face in faces:
            face_str = " ".join(str(int(index) + 1) for index in face)  # Convert to 1-based indexing
            obj_file.write(f"f {face_str}\n")
        #obj_file.write("f 7 9 11 0\n")


def connectQuadVertexOntoTriangle(triMeshFile, quadMeshFile, outputFile):
    # create a mesh of both files.
    triMesh = SurfaceMesh.FromOBJ_FileName(triMeshFile)
    quadMesh = SurfaceMesh.FromOBJ_FileName(quadMeshFile)

    #choose a vertex from the quad mesh
    chosenVertex = quadMesh.vs[30]

    #find the closest triangle vertice
    # loop through all vertices in the triangle mesh
    minDistance = linalg.norm(chosenVertex - triMesh.vs[0])
    closestVertex = triMesh.vs[0]
    index = 0
    vertexIndex = 0
    for vertex in triMesh.vs:
        #calculate the distance between the chosen vertex and the current vertex
        distance = linalg.norm(chosenVertex - vertex)
        #track the vertex with min distance
        if distance < minDistance:
            minDistance = distance
            closestVertex = vertex
            vertexIndex = index
        index += 1

    #find and store each triangle face connected to the closest vertice
    #use the half edge data structure to find all faces connected to the closest triangle vertice.
    facesAdjacentToVertex = triMesh.GetFacesAdjacentToVertex(vertexIndex) # these are the indices of the faces adjacent to the closest triangle vertex.

    #using trimesh:

    #use a for loop to go through each adjacent face until one has barycentric coordiantes all between 0 and 1.
    vertexIndicesOfAdjacentFaces = [] # this will store the vertex indices of the faces adjacent to the closest triangle vertex.
    for face in facesAdjacentToVertex:
        vertexIndicesOfAdjacentFaces.append(triMesh.faces[face])

    # faceMeshIndices = triMesh.faces[facesAdjacentToVertex]
    badCoord = True
    closestFaceIndex = -1
    for face in vertexIndicesOfAdjacentFaces:
        closestFaceIndex += 1
        chosenTriFaceVertices = []
        for vert in face:
            chosenTriFaceVertices.append(triMesh.vs[vert])

        #Project to closest point on plane of a triangle.
        #project the quad point onto the triangle
        projectedPoint = project_point_onto_triangle_plane(chosenVertex, chosenTriFaceVertices[0], chosenTriFaceVertices[1], chosenTriFaceVertices[2])

        #use barycentric coordinates to express it.
        barycentric = convertToBarycentric(projectedPoint, chosenTriFaceVertices[0], chosenTriFaceVertices[1], chosenTriFaceVertices[2])
        print("DEBUG")
        print(barycentric)
        if barycentric[0] >= 0 and barycentric[0] <= 1 and barycentric[1] >= 0 and barycentric[1] <= 1 and barycentric[2] >= 0 and barycentric[2] <= 1:
            badCoord = False
            break

    #if none of them had barycentric coordinates all between 0 and 1, find the closest face and use its barycentric coordinates.
    closestProjectedPointOnEdge = "unassigned"
    if badCoord:
        print("No face with barycentric coordinates all between 0 and 1")
        # Unless there is a way to determine which edges are on the outside, closest to our point, then
        # we need to check all the edges on each adjacent face and use the one with the smallest distance.
        print(facesAdjacentToVertex)
        faceIndex = 0
        for face in facesAdjacentToVertex:
            # get the halfedges of the face.
            # use to_vertex and opposite_edge -> to_vertex to get the vertices of the edges.
            # Do it for all edges until at the first. 
            # Keep the smallest distance then move to next face.
            edges = triMesh.get_face_halfedges(face)
            minDistance = -1
            edgeIndex = 0
            for edge in edges:
                v0 = triMesh.vs[edge.ToVertex()]
                v1 = triMesh.vs[triMesh.halfedges[edge.next_he].ToVertex()]
                #v1 = triMesh.vs[edge.next_he.ToVertex()]
                projectedPointOnEdge , distance = project_point_onto_triangle_edge(projectedPoint, v0, v1)
                if minDistance < 0:
                    minDistance = distance
                if distance < minDistance:
                    minDistance = distance
                    closestFaceIndex = faceIndex
                    closestEdgeIndex = edgeIndex
                    closestProjectedPointOnEdge = projectedPointOnEdge
                edgeIndex += 1
            faceIndex += 1

        #add the vertices in the closest face to a list, then use them to get the barycentric coordinates after
        #finding the closest face and projecting the point onto the edge.
        chosenTriFaceVertices = []
        for vert in triMesh.faces[closestFaceIndex]:
            chosenTriFaceVertices.append(triMesh.vs[vert])
        barycentric = convertToBarycentric(closestProjectedPointOnEdge, chosenTriFaceVertices[0], chosenTriFaceVertices[1], chosenTriFaceVertices[2])

        ########################

    
    #otherwise, keep moving

    #Store the triangle and barycentric coordinates.
    closestFaceMeshIndex = facesAdjacentToVertex[closestFaceIndex]
    #chosenTriFaceVertices - the triangle face vertices list
    #barycentric - the barycentric coordinates of the projected point

    #Output: map from given quadrilateral vertex to triangle barycentric coordinates and triangle index.
    # Form: 
    # 1. Quad Mesh Chosen Vertex values
    # 2. The coordinates of the point after projection onto triangle.
    # 3. Barycentric Coordinates of Projection
    # 4. Closest Triangle Face Index
    # 5. Closest Vertex values on Triangle.


    print("Quad Mesh Chosen Vertex: " + str(chosenVertex))
    print("Projected Point on Triangle: " + str(closestProjectedPointOnEdge))
    print("Barycentric Coordinates of Projection: " + str(barycentric))
    print("Triangle Face Index: " + str(closestFaceMeshIndex))
    print("Closest Vertex on Triangle: " + str(closestVertex))

    import numpy

    #The value will be "unasigned" if 
    #the closest projected point on edge was not assigned, 
    # if it has changed, we can move forward using the point it changed to.
    if isinstance(closestProjectedPointOnEdge, str):
        chosenVertex = [chosenVertex]
        triMesh.vs = numpy.append(triMesh.vs, chosenVertex, axis=0)
    else:
        #This branch is not tested.
        closestProjectedPointOnEdge = [closestProjectedPointOnEdge]
        triMesh.vs = numpy.append(triMesh.vs, closestProjectedPointOnEdge, axis=0)
    save_to_obj(outputFile, triMesh.vs, triMesh.faces)



#connectQuadVertexOntoTriangle("objects/tri_mesh.obj", "objects/tri_mesh1000.obj", "output/SeparateFileTestOutput1.obj")
