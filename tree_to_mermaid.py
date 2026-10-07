import os

def generate_mermaid(startpath):
    print("```mermaid")
    print("graph TD;")
    print('    root["📁 . (Raiz)"];')
    
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '.ssh' in root:
            continue
        
        relpath = os.path.relpath(root, startpath)
        if relpath == ".":
            parent = "root"
        else:
            parent = relpath.replace(os.sep, "_").replace("-", "_").replace(".", "_")
            # Conectar directorio de primer nivel con root si es necesario
            if os.path.dirname(relpath) == "":
                print(f"    root --> {parent}[\"📁 {os.path.basename(relpath)}\"];")
        
        for d in dirs:
            if d.startswith('.'): continue
            child = f"{parent}_{d}".replace("-", "_").replace(".", "_")
            print(f"    {parent} --> {child}[\"📁 {d}\"];")
            
        for f in files:
            if f.startswith('.'): continue
            child = f"{parent}_{f.replace('.', '_')}".replace("-", "_")
            print(f"    {parent} --> {child}[\"📄 {f}\"];")
            
    print("```")

generate_mermaid(".")
