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

#----------------------------------------#
# This script use xinntao/Real-ESRGAN-ncnn-vulkan to upscale the images
# You can download it from : https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases
# Choose release for your operating system, unzip the file on your hard drive.
#----------------------------------------#

import os
import subprocess
import bpy

# path to realesrgan-ncnn-vulkan executable.
# on Linux render the file executable
# on Windows, use "/" or "\\" in path
#path_to_real_esrgan = "C:/Users/franck/Documents/Dvp/Real-ESRGAN/realesrgan-ncnn-vulkan.exe"
path_to_real_esrgan = "/home/franck/Softs/Real-ESRGAN/realesrgan-ncnn-vulkan"

# Choose a scale from 2, 3 or 4 
# The render resolution will be divided by this value and then the images scaled by the same ratio.
scale = 4 # 2, 3 or 4

# Render animation (True) or current frame (False)
render_animation = False

# model
models = [
    'realesrgan-x4plus',        # 0
    'realesrnet-x4plus',        # 1
    'realesrgan-x4plus-anime',  # 2
    'realesr-animevideov3'      # 3
]
model = 0


def get_file_path():
    if not bpy.data.is_saved:
        raise IOError('The file must be saved')
    
    filepath = bpy.data.filepath
    return os.path.basename(filepath), os.path.dirname(filepath)

def create_dir(dir_path, dir_name):
    dir = os.path.join(dir_path, dir_name)
    if not os.path.isdir(dir):
        os.mkdir(dir) 
    return dir

def upscale(input, output, scale):
    subprocess.call([
        path_to_real_esrgan, 
        "-i", 
        input,
        "-o", 
        output,
        "-s",
        str(scale),
        "-n",
        models[model]
    ])
        
def main():
    scene = bpy.context.scene
    
    file_name, dir_path = get_file_path()
    render_dir = create_dir(dir_path, f"render_{file_name[:-6]}")
    
    frame_current = scene.frame_current
    extension = scene.render.file_extension
    
    output = os.path.join(render_dir, 'img_')
    if not render_animation:
        output = os.path.join(render_dir, f"image_{frame_current:04d}")
    scene.render.filepath = os.path.join(render_dir, output)
    
    initial_x = scene.render.resolution_x
    initial_y = scene.render.resolution_y
    
    scene.render.resolution_x = round(initial_x / scale)
    scene.render.resolution_y = round(initial_y / scale)
    
    render_upscaled = create_dir(render_dir, f"{models[model]}_x{scale}")
    
    scene['render_dir'] = render_dir
    scene['render_upscaled'] = render_upscaled
    scene['scale'] = scale
    scene['render_animation'] = render_animation
    scene['frame_current'] = scene.frame_current
    scene['extension'] = extension
    
    bpy.ops.render.render('INVOKE_DEFAULT', animation=render_animation, write_still= not render_animation)
    
    scene.render.resolution_x = initial_x
    scene.render.resolution_y = initial_y
    
def render_complete(scene):
    print('Render Complete')
    print('---------------')
    print('Start upscale...')
    print('---------------')
    
    input = scene['render_dir']
    output = scene['render_upscaled']
    if not scene['render_animation']:
        name = f"image_{scene['frame_current']:04d}{scene['extension']}"
        input = os.path.join(input, name)
        output = os.path.join(output, name)
            
    upscale(
        input, 
        output,
        scene['scale']
    )
    print('---------------')    
    print("images upscaled")
      
if __name__ == "__main__":
    if not render_complete.__name__ in [hand.__name__ for hand in bpy.app.handlers.render_complete]:
        bpy.app.handlers.render_complete.append(render_complete)
    main()