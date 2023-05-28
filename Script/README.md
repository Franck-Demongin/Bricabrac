# SCRIPT

## Object Slicer

_File: **object_slicer.py**_

![script_object_slicer](https://user-images.githubusercontent.com/54265936/167301730-148dcc4b-ba5a-4a43-8f87-c76f1d136465.png)

Cut mesh in blocks

Adjust number of blocks in X, Y and Z

```
# Nombre de tranche sur X
x = 4
# Nombre de tranche sur Y
y = 4
# Nombre de tranche sur Z
z = 4
```
Select an object and run script.

## Export glTF

_File: **export_gltf.py**_

![Export_glTF](https://user-images.githubusercontent.com/54265936/201516252-ba66d5d4-3395-40f5-9836-b45d949582ce.png)

Export all visible objects in the scene of type MESH in single glTF file.

Adjust PATH to export object in folder of your choice.

On Linux:
```
PATH = '/Path/to/folder' 
```

On Windows:
```
PATH = 'C:/path/to/folder' # use /
```

## Key Configuration

_File: **keyconfig_list.py**_

![script_keyconfig_list](https://user-images.githubusercontent.com/54265936/213939029-6f81af65-0231-4578-b709-6091bccd549e.png)

List all shortcuts in a text file.

Save .blend file before run script.  
A file named kc.txt will be created in the same folder.

## Auto Bake Indirect Lighting

_File: **auto_bake_indirect_lighting.py**_

![script_auto_bake_indirect_lighting](https://user-images.githubusercontent.com/54265936/214378253-8c246d12-3e25-4f4c-b143-d9a785edd029.png)

Export animation to PNG images sequence. Images are saved in **_Output Path_**.  
Bake indirect lighting before render each frame.

Images are displayed in UI (a 3D View or an Image Editor must be open) and the render coulb be interrupt by press 'ESC'.

## Unwrap in 3D View

_File: **unwrap_in_3dview.py**_

![script_unwrap_in_3dview](https://github.com/Franck-Demongin/Bricabrac/assets/54265936/4b7d0618-d619-4b14-b00e-d552cb1bc368)

Allows you to unfold a mesh following these UVs in the 3D view. 
Add seams and unwrap your mesh before run the script.
The _copy_ variable at the beginning of the script can be set to False or True. If it is True, a copy of the object is made before unfolding.

## Upscale render with Real-ESRGAN

_File: **upscale_real_esrgan.py**_

![script_upscale_real-esrgan](https://github.com/Franck-Demongin/Bricabrac/assets/54265936/a8d59e53-9f57-4c5f-9322-2b9f1f3bfce4)

This script use xinntao/Real-ESRGAN-ncnn-vulkan to upscale the render image.
You can download it from : [xinntao/Real-ESRGAN-ncnn-vulkan/releases](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases)
Choose release for your operating system, unzip the file on your hard drive.


### Usage
In the script, update path_to_real_esrgan to the executable.
Choose a scale from 2, 3 or 4 
The render resolution will be divided by this value and then the images scaled by the same ratio.
For example, if the render resolution is 1980x1080 px and the scale is 4, the script render each frame at 480x270 px and
the final images are upscaled by 4 to make 1980x1080 px.
The script create a render folder in the same directory of the blend file. It will fail if the blend file is not saved.
The render folder name is to the form : blendfile_name(without extension).
The upscaled images are in a sub-folder named like scale selected. Ex : x4 or x3
