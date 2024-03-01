import bpy

def clear_existing_objects():
    """Clears existing mesh objects in the scene."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def create_material(name, color):
    """Creates and returns a new material with the specified name and color."""
    material = bpy.data.materials.new(name=name)
    material.diffuse_color = color
    return material

def create_mesh_object(mesh_name, object_name, vertices, material):
    """Creates a new mesh object with the specified name, vertices, and material."""
    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(object_name, mesh)
    obj.location = bpy.context.scene.cursor.location
    bpy.context.collection.objects.link(obj)

    obj.data.materials.append(material)

    mesh.from_pydata(vertices, [], [(0, 1, 2)])
    mesh.update()

def draw_sierpinski(x1, y1, x2, y2, x3, y3, depth, colors):
    """Recursively draws the Sierpinski triangle with specified depth and colors."""
    global num
    if depth > 0:
        num += 1
        # Calculate midpoints
        midx1 = (x1 + x2) / 2
        midy1 = (y1 + y2) / 2
        midx2 = (x2 + x3) / 2
        midy2 = (y2 + y3) / 2
        midx3 = (x1 + x3) / 2
        midy3 = (y1 + y3) / 2

        # Recursively draw smaller triangles
        draw_sierpinski(x1, y1, midx1, midy1, midx3, midy3, depth - 1, colors)
        draw_sierpinski(midx1, midy1, x2, y2, midx2, midy2, depth - 1, colors)
        draw_sierpinski(midx3, midy3, midx2, midy2, x3, y3, depth - 1, colors)
    else:
        # Create material for the triangle
        material = create_material(f"SierpinskiMaterial_{num}", colors[num % len(colors)])

        # Create mesh and object for the triangle
        create_mesh_object(f"SierpinskiTriangleMesh_{num}", f"SierpinskiTriangle_{num}",
                           [(x1, y1, 0), (x2, y2, 0), (x3, y3, 0)], material)

def main():
    """Main function to draw the Sierpinski triangle."""
    clear_existing_objects()

    global num
    num = 0  # Counter for the number of recursions

    # Define initial vertices of the base triangle
    vertices = [(-1, -1, 0), (1, -1, 0), (0, 1, 0)]
    # Define initial depth of recursion
    depth = 2
    # Define colors (RGBA values) for the triangles
    colors = [
        (0.0, 0.0, 1.0, 1.0),  # Blue
        (1.0, 0.0, 0.0, 1.0),  # Red
        (0.0, 1.0, 0.0, 1.0),  # Green
    ]

    # Start drawing the Sierpinski triangle
    draw_sierpinski(vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1], depth, colors)

if __name__ == "__main__":
    main()
