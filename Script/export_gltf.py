import os
import bpy

PATH = "/home/franck/Bureau/"

objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and  o.visible_get() == True and not o.hide_viewport]

for o in objs:
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    filepath = os.path.join(PATH, o.name)
    bpy.ops.export_scene.gltf(
        filepath=filepath, 
        export_format='GLB',
        use_selection=True, 
        export_apply=True
    )