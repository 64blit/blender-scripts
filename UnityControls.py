import bpy

def setup_unity_like_keymap():
    for keymap in bpy.context.window_manager.keyconfigs.user.keymaps:
        if keymap.space_type in ('EMPTY', 'NODE_EDITOR', 'IMAGE_EDITOR'):
            # Add View2D RMB pan
            if keymap.name == 'Image':
                add_key_to_keymap(keymap, 'image.view_pan', 'MOUSE', 'RIGHTMOUSE', 'CLICK_DRAG')
            if keymap.name == "View2D":
                add_key_to_keymap(keymap, 'view2d.pan', 'MOUSE', 'RIGHTMOUSE', 'CLICK_DRAG')

            for key in keymap.keymap_items:
                if not any([key.any, key.alt, key.ctrl, key.shift]):
                    if key.map_type == 'MOUSE' and key.type == 'RIGHTMOUSE' and key.value != 'CLICK_DRAG':
                        key.value = 'CLICK'

    for keymap in bpy.context.window_manager.keyconfigs.user.keymaps:
        if keymap.space_type == 'VIEW_3D':
            for key in keymap.keymap_items:
                if key.idname == 'view3d.rotate' and key.map_type == 'MOUSE':
                    key.type = 'RIGHTMOUSE'
                    key.value = 'CLICK_DRAG'
                    key.any = False
                    key.alt = False
                    key.ctrl = False
                    key.shift = False
                elif key.idname == 'view3d.move' and key.map_type == 'MOUSE':
                    key.type = 'MIDDLEMOUSE'
                    key.value = 'CLICK_DRAG'
                    key.any = False
                    key.alt = False
                    key.ctrl = False
                    key.shift = False

def add_key_to_keymap(keymap, idname, map_type, type, value, any=False, shift=0, ctrl=0, alt=0, oskey=0, key_modifier='NONE', repeat=False, head=False):
    for key in keymap.keymap_items:
        if key.idname == idname and key.map_type == map_type and key.type == type and key.value == value and key.any == any and key.alt == alt and key.ctrl == ctrl and key.shift == shift:
            key.active = True
            break
    else:
        keymap.keymap_items.new(idname=idname, type=type, value=value, any=any, shift=shift, ctrl=ctrl, alt=alt, oskey=oskey, key_modifier=key_modifier, repeat=repeat, head=head)


def focus_on_object():
    for keymap in bpy.context.window_manager.keyconfigs.user.keymaps:
        if keymap.space_type == 'VIEW_3D':
            add_key_to_keymap(keymap, 'view3d.view_selected', 'KEYBOARD', 'F', 'PRESS')


if __name__ == "__main__":
    setup_unity_like_keymap()
    focus_on_object()
