import bpy
import bmesh

# Get the active object and ensure it's in edit mode
obj = bpy.context.active_object
if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
    raise Exception("Please select a mesh and enter Edit Mode")

# Get the selected vertex
bm = bmesh.from_edit_mesh(obj.data)
selected_verts = [v for v in bm.verts if v.select]

if len(selected_verts) != 1:
    raise Exception("Please select exactly one vertex to start the path from.")

# Starting vertex (the one selected by the user)
start_vertex = selected_verts[0]

# Function to find the next connected vertex
def find_next_vertex(current_vertex, visited_vertices):
    for edge in current_vertex.link_edges:
        next_vert = edge.other_vert(current_vertex)
        if next_vert not in visited_vertices:
            return next_vert
    return None

# List to store the new ordering of vertices
new_order = []

# Set to keep track of visited vertices
visited = set()

# Start from the selected vertex
current_vertex = start_vertex

# Traverse the path
while current_vertex is not None:
    # Mark this vertex as visited
    visited.add(current_vertex)
    
    # Append to new_order for later processing
    new_order.append(current_vertex)
    
    # Find the next connected vertex
    current_vertex = find_next_vertex(current_vertex, visited)

# Create a new mesh and new object
new_mesh = bpy.data.meshes.new("reordered_mesh")
new_bm = bmesh.new()

# Create new vertices based on the new order
vert_map = {}  # Map old vertex to new vertex for referencing in face and edge creation
for v in new_order:
    new_vert = new_bm.verts.new(v.co)
    vert_map[v] = new_vert

# Ensure all geometry is updated in bmesh
new_bm.verts.ensure_lookup_table()

# Create faces in the new bmesh based on the old faces
for face in bm.faces:
    try:
        new_face_verts = [vert_map[v] for v in face.verts]
        new_bm.faces.new(new_face_verts)
    except ValueError:
        # If face creation fails due to degenerate geometry, skip it
        continue

# Create edges between the new vertices in the new order
for i in range(len(new_order) - 1):
    v1 = vert_map[new_order[i]]
    v2 = vert_map[new_order[i + 1]]
    new_bm.edges.new((v1, v2))

# Finish up and write the new bmesh to the new mesh
new_bm.to_mesh(new_mesh)
new_bm.free()

# Create a new object and link it to the current collection
new_obj = bpy.data.objects.new(obj.name, new_mesh)
bpy.context.collection.objects.link(new_obj)

# Set the new object to the same transformation as the old one
new_obj.location = obj.location
new_obj.rotation_euler = obj.rotation_euler
new_obj.scale = obj.scale

# Rename the original object
obj.name = obj.name + "_old"

# Hide the original object
obj.hide_set(True)

# Update context to set the new object as active
bpy.context.view_layer.objects.active = new_obj
new_obj.select_set(True)

# Set the mode to OBJECT and then back to EDIT to refresh and ensure everything is properly set
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')

print(f"Created a new object '{new_obj.name}' with reordered vertices connected by edges. The original object '{obj.name}' has been hidden.")
