import os

def generate_mermaid(startpath):
    print("```mermaid")
    print("graph TD;")
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '.ssh' in root:
            continue
        relpath = os.path.relpath(root, startpath)
        parent = relpath.replace(os.sep, "_").replace("-", "_") if relpath != "." else "root"
        
        for d in dirs:
            if d.startswith('.'): continue
            child = f"{parent}_{d}".replace("-", "_")
            print(    f"{parent} --> {child}[\"📁 {d}\"];")
            
        for f in files:
            if f.startswith('.'): continue
            child = f"{parent}_{f.replace('.', '_')}"
            print(    f"{parent} --> {child}[\"📄 {f}\"];")
            
    print("```")

generate_mermaid(".")
