# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from mathutils import Vector

# Nombre de tranche sur X
x = 4
# Nombre de tranche sur Y
y = 4
# Nombre de tranche sur Z
z = 4
 
def bounds(obj, local=False):
 
    local_coords = obj.bound_box[:]
    om = obj.matrix_world
 
    if not local:
        worldify = lambda p: om @ Vector(p[:]) 
        coords = [worldify(p).to_tuple() for p in local_coords]
    else:
        coords = [p[:] for p in local_coords]
        
    rotated = zip(*coords[::-1])
    
    push_axis = []
    for (axis, _list) in zip('xyz', rotated):
        info = lambda: None
        info.max = max(_list)
        info.min = min(_list)
        info.distance = info.max - info.min
        push_axis.append(info)
    
    import collections
    
    originals = dict(zip(['x', 'y', 'z'], push_axis))
     
    o_details = collections.namedtuple('object_details', 'x y z')
    return o_details(**originals)

obj = bpy.context.object

index = [0,0]

if obj is not None:

    bounds = bounds(obj)
    # print(bounds.z.max)
    
    pas_x = bounds.x.distance / x
    pas_y = bounds.y.distance / y
    pas_z = bounds.z.distance / z
    
    min_x = bounds.x.min 
    min_y = bounds.y.min
    min_z = bounds.z.min
        
    # for cell_id in list(range(1, (x * y) + 1)):
    for row in list(range(0, x)):
        for col in list(range(0, y)):
            for item in list(range(0, z)):
                print(row, col)
                copy = bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
                bpy.ops.object.editmode_toggle()
                
                offset = min_x + (row * pas_x) 
                offset1 = min_x + ((row+1) * pas_x)
                
                bpy.ops.mesh.bisect(plane_co=(offset, 0, 0), plane_no=(1, 0, 0), use_fill=True, clear_inner=True, clear_outer=False, flip=False)
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=(offset1, 0, 0), plane_no=(1, 0, 0), use_fill=True, clear_inner=False, clear_outer=True, flip=False)

                bpy.ops.mesh.select_all(action='SELECT')
                
                offset = min_z + (item * pas_z) 
                offset1 = min_z + ((item+1) * pas_z)
                
                bpy.ops.mesh.bisect(plane_co=(0, 0, offset), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, clear_outer=False, flip=False)
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=(0, 0, offset1), plane_no=(0, 0, 1), use_fill=True, clear_inner=False, clear_outer=True, flip=False)
                
                bpy.ops.mesh.select_all(action='SELECT')
                
                offset = min_y + (col * pas_y) 
                offset1 = min_y + ((col+1) * pas_y)
                
                bpy.ops.mesh.bisect(plane_co=(0, offset, 0), plane_no=(0, 1, 0), use_fill=True, clear_inner=True, clear_outer=False, flip=False)
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=(0, offset1, 0), plane_no=(0, 1, 0), use_fill=True, clear_inner=False, clear_outer=True, flip=False)
                
                offset = min_z + (item * pas_z) 
                offset1 = min_z + ((item+1) * pas_z)
                
                bpy.ops.mesh.bisect(plane_co=(0, 0, offset), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, clear_outer=False, flip=False)
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.bisect(plane_co=(0, 0, offset1), plane_no=(0, 0, 1), use_fill=True, clear_inner=False, clear_outer=True, flip=False)
                
                bpy.ops.object.editmode_toggle()
                
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                
                bpy.ops.object.select_all(action='DESELECT')
                
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)            

            

            
            

            
        
    
    
    
    
    