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
