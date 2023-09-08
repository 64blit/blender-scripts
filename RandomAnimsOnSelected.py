import bpy
import random

# Set the number of frames for the animation
start_frame = 1
end_frame = 100
num_keyframes = 6  # Number of keyframes including the start and end frames
random_frame_factor = 2  # Factor to add randomness to the frame

# Function to change keyframe interpolation mode to linear
def set_interpolation(curves):
    for curve in curves:
        for kp in curve.keyframe_points:
            kp.interpolation = 'LINEAR'

# Clear existing keyframes and update existing action with equal spacing and linear interpolation
for obj in bpy.context.selected_objects:
    if obj.animation_data:
        action = obj.animation_data.action
        if action:
            # Clear existing keyframes
            for fcurve in action.fcurves:
                fcurve.keyframe_points.clear()

            # Select the object and set its location at the start frame
            bpy.context.view_layer.objects.active = obj
            initial_location = obj.location.copy()  # Store the initial location
            initial_scale = obj.scale.copy()  # Store the initial scale
            
            # Calculate the step size to evenly space the keyframes
            step_size = (end_frame - start_frame) / (num_keyframes - 1)
            
            # Create keyframes with equal spacing and linear interpolation within the animation range
            for i in range(num_keyframes):
                frame = int(start_frame + i * step_size + random.uniform(-random_frame_factor, random_frame_factor))
                
                if frame == 1 or frame == end_frame:
                    # For the first keyframe, don't apply randomization
                    obj.location = initial_location
                    obj.scale = initial_scale
                else:
                    obj.location.x += random.uniform(-0.1, 0.1)  # Manually move X with randomization
                    obj.location.y += random.uniform(-0.1, 0.1)  # Manually move Y with randomization
                    obj.location.z += random.uniform(-0.1, 0.1)  # Manually move Z with randomization

                obj.keyframe_insert(data_path="location", frame=frame)
                obj.keyframe_insert(data_path="scale", frame=frame)

            # Create a keyframe at the end frame to match the initial position and scale
            obj.keyframe_insert(data_path="location", frame=end_frame)
            obj.keyframe_insert(data_path="scale", frame=end_frame)

            # Set keyframe interpolation mode to linear for location and scale
            set_interpolation(action.fcurves)

            # Set custom property "LoopingAnimations" to the object's current action name
            obj["LoopingAnimations"] = action.name

print("Existing keyframes cleared, existing animation action updated with equal distance apart keyframes, manual location with increased random range (except for the first keyframe), and subtle scale changes, ending with initial position and scale, linear interpolation set, and custom property 'LoopingAnimations' updated for selected objects.")
