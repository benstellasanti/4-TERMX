import os

def generate_mermaid_string():
    lines = []
    lines.append("```mermaid")
    lines.append("graph TD;")
    lines.append('    root["📁 . (Raiz)"];')
    
    startpath = "."
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '.ssh' in root or '__pycache__' in root:
            continue
        
        relpath = os.path.relpath(root, startpath)
        if relpath == ".":
            parent = "root"
        else:
            parent = relpath.replace(os.sep, "_").replace("-", "_").replace(".", "_")
            if os.path.dirname(relpath) == "":
                lines.append(f"    root --> {parent}[\"📁 {os.path.basename(relpath)}\"];")
        
        for d in dirs:
            if d.startswith('.'): continue
            child = f"{parent}_{d}".replace("-", "_").replace(".", "_")
            lines.append(f"    {parent} --> {child}[\"📁 {d}\"];")
            
        for f in files:
            if f.startswith('.') or f == "update_readme_tree.py": continue
            child = f"{parent}_{f.replace('.', '_')}".replace("-", "_")
            lines.append(f"    {parent} --> {child}[\"📄 {f}\"];")
            
    lines.append("```")
    return "\n".join(lines)

def update_readme():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_mermaid = generate_mermaid_string()
    
    start_tag = "<!-- START_TREE_DIAGRAM -->"
    end_tag = "<!-- END_TREE_DIAGRAM -->"

    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        updated_content = content[:start_idx] + "\n" + new_mermaid + "\n" + content[end_idx:]
    else:
        # Si no existen las etiquetas, las añade al final
        updated_content = content + f"\n\n## 📂 Estructura del Repositorio\n{start_tag}\n{new_mermaid}\n{end_tag}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()
