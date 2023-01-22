import os
import bpy

def save_kc(data, ext):
    if not bpy.data.is_saved:
        print("ERROR : Saved file before run script")    
        return        
    path = os.path.dirname(bpy.data.filepath)
    with open(os.path.join(path, f"kc.{ext}"), 'w') as f:
        f.write(data)

def kc_to_string(kc):
    output = ''
    for cat in kc:
        output += f"{(len(cat.name) + 4)*'#'}\n"
        output += f"# {cat.name} #\n"
        output += f"{(len(cat.name) + 4)*'#'}\n"        
        for item in cat.keymap_items:
            output += f"{item.name}"            
            if item.properties:
                if 'space_type' in item.properties:
                    output += f" /{item.properties.space_type}"
                if 'direction' in item.properties:
                    output += f" /{item.properties.direction}"
            output += " >> "
            output += f"{item.to_string()}\n"        
        output += "\n"    
    return output    

def main():
    kc = bpy.context.window_manager.keyconfigs.user.keymaps
    str = kc_to_string(kc)

    print(str)
    save_kc(str, 'txt')

if __name__ == "__main__":
    main()
    
