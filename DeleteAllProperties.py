# a blender python script to remove all custom properties on all selected objects

# (c) 2018 by github.com/nortikin
# License: MIT
import bpy
for o in bpy.context.selected_objects:
    for p in o.keys():
        if p not in ['location', 'rotation_euler', 'rotation_quaternion', 'rotation_axis_angle', 'scale', 'dimensions', 'delta_location', 'delta_rotation_euler', 'delta_rotation_quaternion', 'delta_scale', 'lock_location', 'lock_rotation', 'lock_rotation_w', 'lock_rotations_4d', 'lock_rotations_interpolation', 'lock_scale', 'matrix_basis', 'matrix_local', 'matrix_parent_inverse', 'matrix_world', 'modifiers', 'name', 'parent', 'parent_bone', 'parent_type', 'pose', 'proxy', 'rigid_body', 'rotation_mode', 'show_bounds', 'show_name', 'type', 'up_axis', 'use_slow_parent', 'use_slow_parent_inverse', 'visible_get', 'visible_in_viewport_get', 'xray']):
            del o[p]
