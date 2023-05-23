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

copy = False

def poll(context):
    obj = context.object
    if obj is None or obj.type != 'MESH':
        raise TypeError("An object of type MESH must be selected")
    
    return True

def split_seams(obj):
    """
    Split edge seams
    """

    faces = obj.data.polygons
    edges = obj.data.edges
    verts = obj.data.vertices
    for f in faces:                   
        f.select=False               
    for e in edges:
        e.select=False
    for v in verts:
        v.select=False
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bpy.ops.object.mode_set(mode='OBJECT')
        
    for e in edges:
        e.select = e.use_seam    
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.edge_split()
    bpy.ops.object.mode_set(mode='OBJECT')

def unwrap_in_3dview(obj):
    """
    Unfold the mesh according to its UVs
    """
        
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
        
def duplicate(obj, copy):
    """
    Duplicate the object if copy is True
    """
    
    if copy:
        bpy.ops.object.duplicate_move()
        obj = bpy.context.object
    return obj

def get_object(context, copy):
    """
    Return object or copy and initial location if type is mesh or raise an TypeError
    """
    
    bpy.ops.object.mode_set(mode='OBJECT')
    obj = context.object
    obj.select_set(True)
    return duplicate(obj, copy), obj.location.copy()
    
def position_object(obj, base_loc):
    """
    Set the origin of the object to the geometry and set the position
    """
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj.location.x = base_loc.x
    obj.location.y = base_loc.y
        
def main():
    context = bpy.context

    poll(context)
    
    obj, base_loc = get_object(context, copy)  
    split_seams(obj)
    unwrap_in_3dview(obj)    
    position_object(obj, base_loc)

if __name__ == "__main__":
    main()
