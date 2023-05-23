import bpy
from mathutils import Vector

copy = True

def unwrap_in_3dview(obj):
    for f in obj.data.polygons:
        if f.index == 0:
            vert1 = f.vertices[0]
            vert2 = f.vertices[1]
            pos1 = obj.data.vertices[vert1].co
            pos2 = obj.data.vertices[vert2].co

            length = (pos1 - pos2).length
            
        for vert_idx, loop_idx in zip(f.vertices, f.loop_indices):
            if f.index == 0:
                if vert_idx == vert1:
                    uv_pos1 = obj.data.uv_layers.active.data[loop_idx].uv
                if vert_idx == vert2:
                    uv_pos2 = obj.data.uv_layers.active.data[loop_idx].uv
        
        uv_length = (Vector(uv_pos1) - Vector(uv_pos2)).length        
        scale = length / uv_length
               
        for vert_idx, loop_idx in zip(f.vertices, f.loop_indices):
            uv_co = obj.data.uv_layers.active.data[loop_idx].uv
            obj.data.vertices[vert_idx].co = Vector((uv_co.x, uv_co.y, 0)) * scale
        

def get_mesh(context, copy):
    obj = context.object
    if obj is None or obj.type != 'MESH':
        raise TypeError("An object of type MESH must be active")
    obj.select_set(True)
    return duplicate(obj, copy), obj.location.copy()
    
def duplicate(obj, copy):
    if copy:
        bpy.ops.object.duplicate_move()
        obj = bpy.context.object
    return obj

def position_object(obj, base_loc):
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj.location.x = base_loc.x
    obj.location.y = base_loc.y
        
def main():
    context = bpy.context
    
    obj, base_loc = get_mesh(context, copy)  
    print(base_loc)  
    unwrap_in_3dview(obj)    
    position_object(obj, base_loc)

if __name__ == "__main__":
    main()
