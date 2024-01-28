import bpy
import os
import sys

# parameters
argv = sys.argv
argv = argv[argv.index("--") + 1:]

ply_filepath = argv[0]
ply_filepath = os.path.abspath(ply_filepath)

basename_without_ext = os.path.basename(ply_filepath).split('.')[0]
os.makedirs(f'fbx/{basename_without_ext}', exist_ok=True)

png_filepath = f'fbx/{basename_without_ext}/{basename_without_ext}.png'
png_filepath = os.path.abspath(png_filepath)
fbx_filepath = f'fbx/{basename_without_ext}/{basename_without_ext}.fbx'
fbx_filepath = os.path.abspath(fbx_filepath)

# clear all mesh data
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# load the .ply file
bpy.ops.import_mesh.ply(filepath=ply_filepath)

# get the current object
obj = bpy.context.scene.objects[-1]
# obj = bpy.context.active_object

# Get the 3D view area
view3d_area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
print(view3d_area)

# Set the shading type to 'SOLID'
view3d_area.spaces[0].shading.type = 'SOLID'

# Set the shading color to 'VERTEX'
view3d_area.spaces[0].shading.color_type = 'VERTEX'

# create a new image
image = bpy.data.images.new('BakedImage', width=1024, height=1024)

# Ensure the object is active and selected
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Enter edit mode
bpy.ops.object.mode_set(mode='EDIT')

# Get current number of polygons an set ratio of decimation
num_polygons = len(obj.data.polygons)
# The actual number of polygons may not match the specified count. 
# It is advisable to consider approximately twice the desired polygon count as a baseline.
target_num_polygons = 3000
ratio = target_num_polygons / num_polygons

# Set decimate modifier
bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers["Decimate"].ratio = ratio

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Apply decimate modifier 
bpy.ops.object.modifier_apply(modifier="Decimate")

# Enter edit mode
bpy.ops.object.mode_set(mode='EDIT')

# Select all mesh elements
bpy.ops.mesh.select_all(action='SELECT')

# Create a new UV map with smart UV project
bpy.ops.uv.smart_project()

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# create a new material
material = bpy.data.materials.new(name='BakedMaterial')
obj.data.materials.append(material)

# Enable 'Use Nodes'
material.use_nodes = True

# get the Principled BSDF node
bsdf = material.node_tree.nodes["Principled BSDF"]

# create an Attribute node and set its attribute name
attribute_node = material.node_tree.nodes.new('ShaderNodeAttribute')
attribute_node.attribute_name = "Col"  # Replace "Col" with the name of your color attribute

# Connect the Attribute node color to the Principled BSDF node's Base Color
material.node_tree.links.new(bsdf.inputs['Base Color'], attribute_node.outputs['Color'])

# Change the screen to the shading workspace
for screen in bpy.data.screens:
    if "Shading" in screen.name:
        bpy.context.window.screen = screen

# create a new image texture node
texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')

# assign the image to the texture node
texture_node.image = image

# select the render engine
bpy.context.scene.render.engine = 'CYCLES'

# set the bake type
bpy.context.scene.cycles.bake_type = 'DIFFUSE'

# set the bake parameters
bpy.context.scene.render.bake.use_pass_direct = False
bpy.context.scene.render.bake.use_pass_indirect = False
bpy.context.scene.render.bake.use_pass_color = True

# bake the image
bpy.ops.object.bake(type='DIFFUSE')

# save the image
image.filepath_raw = png_filepath
image.file_format = 'PNG'
image.save()

# disconnect the Attribute node color from the Principled BSDF node's Base Color
material.node_tree.links.remove(bsdf.inputs['Base Color'].links[0])

# connect the Image Texture node color to the Principled BSDF node's Base Color
material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])

# check model in 3D view with material
view3d_area.spaces[0].shading.type = 'MATERIAL'

# export the model as .fbx
bpy.ops.export_scene.fbx(filepath=fbx_filepath, use_selection=True)
