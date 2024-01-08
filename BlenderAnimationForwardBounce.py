# write a blender script that creates an animation for all selected objects.
# the animation should be a forward bounce, where the objects move in the -y direction by .5 units, then back to their original position.
# the animation should be 10 frames long, with 3 keyframes.
# the first keyframe is at 1, setting the starting position, the second keyframe is at 5, setting the forward bounce position, and the last keyframe is at 10, resetting the position to the original.
# the interpolation mode should be bounce on all keyframes.
# The name of the animation to the objects name + "_bounce"
import bpy

# Get all selected objects
selected_objects = bpy.context.selected_objects

for obj in selected_objects:
    # Store the original position
    original_position = obj.location.copy()

    # Create new animation data if it doesn't exist
    if obj.animation_data is None:
        obj.animation_data_create()

    # Create a new action
    action_name = obj.name + "_bounce"
    action = bpy.data.actions.new(name=action_name)
    obj.animation_data.action = action

    # Create location keyframes
    for frame in [1, 5, 10]:
        obj.location = original_position
        if frame == 5:
            obj.location.y -= 0.5
        obj.keyframe_insert(data_path="location", frame=frame)

    # Set interpolation mode to 'BOUNCE'
    for fcurve in action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'BOUNCE'

    # Reset the location
    obj.location = original_position
    obj["OnPointerEnterAnimations"] = action.name

