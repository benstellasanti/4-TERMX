import os

def generate_mermaid_string(files_list):
    lines = []
    lines.append("```mermaid")
    lines.append("graph TD;")
    lines.append('    root["📁 . (Raiz)"];')
    
    startpath = "."
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '.ssh' in root or '__pycache__' in root or '.github' in root:
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
            if f == "update_readme_tree.py": continue
            child = f"{parent}_{f.replace('.', '_')}".replace("-", "_")
            lines.append(f"    {parent} --> {child}[\"📄 {f}\"];")
            
    lines.append("```")
    return "\n".join(lines)

def generate_file_table():
    # Descripciones personalizadas estándar para los archivos clave de tu entorno
    descriptions = {
        "README.md": "Documentación central y guía del entorno móvil.",
        "sync-repo.sh": "Script ejecutable para sincronización remota segura vía SSH.",
        "update_readme_tree.py": "Automatización en Python que actualiza el árbol y la tabla del README."
    }
    
    table_lines = []
    table_lines.append("| Archivo / Componente | Propósito en el Entorno |")
    table_lines.append("| :--- | :--- |")
    
    startpath = "."
    for root, dirs, files in os.walk(startpath):
        if '.git' in root or '.ssh' in root or '__pycache__' in root or '.github' in root:
            continue
        for f in files:
            if f == "update_readme_tree.py": continue
            desc = descriptions.get(f, "Archivo de configuración o soporte del sistema.")
            table_lines.append(f"| `📄 {f}` | {desc} |")
            
    return "\n".join(table_lines)

def update_readme():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_mermaid = generate_mermaid_string([])
    new_table = generate_file_table()
    
    start_tag = "<!-- START_TREE_DIAGRAM -->"
    end_tag = "<!-- END_TREE_DIAGRAM -->"

    # Bloque para el diagrama Mermaid
    if start_tag in content and end_tag in content:
        start_idx = content.find(start_tag) + len(start_tag)
        end_idx = content.find(end_tag)
        content = content[:start_idx] + "\n" + new_mermaid + "\n" + content[end_idx:]

    # Bloque para la tabla de archivos descriptivos
    table_start = "<!-- START_FILE_TABLE -->"
    table_end = "<!-- END_FILE_TABLE -->"
    if table_start in content and table_end in content:
        t_start_idx = content.find(table_start) + len(table_start)
        t_end_idx = content.find(table_end)
        content = content[:t_start_idx] + "\n" + new_table + "\n" + content[t_end_idx:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
