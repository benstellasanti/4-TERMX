#!/usr/bin/env python3
"""
svg2canvas.py — Convierte un SVG generado por Graphviz en un archivo
.canvas de Obsidian (formato JSON Canvas). Sin dependencias externas.

Uso:
    python svg2canvas.py diagrama.svg                  # -> diagrama.canvas
    python svg2canvas.py diagrama.svg -o salida.canvas
    python svg2canvas.py diagrama.svg --layout tree-td
    python svg2canvas.py diagrama.svg --layout original --no-color

Layouts:
    auto      (por defecto) árbol si el grafo es un árbol/bosque, si no "original"
    tree-lr   árbol de izquierda a derecha
    tree-td   árbol de arriba abajo
    original  respeta las posiciones del SVG, escaladas para que no se solapen

Si el SVG no es de Graphviz (no tiene grupos class="node"/"edge"), se usa un
modo de respaldo que crea una tarjeta por cada <text> sin conexiones.
"""
import argparse
import hashlib
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NUM = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
LIGHT = {"white", "#fff", "#ffffff", "none", "transparent", "", None}


# ───────────────────────────── utilidades SVG ─────────────────────────────
def strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    return root


def shape_bbox(el):
    """Devuelve (xmin, ymin, xmax, ymax) de polygon/polyline/ellipse/rect/path."""
    t = el.tag
    if t in ("polygon", "polyline"):
        v = list(map(float, NUM.findall(el.get("points", ""))))
        xs, ys = v[0::2], v[1::2]
    elif t == "ellipse":
        cx, cy = float(el.get("cx", 0)), float(el.get("cy", 0))
        rx, ry = float(el.get("rx", 0)), float(el.get("ry", 0))
        return cx - rx, cy - ry, cx + rx, cy + ry
    elif t == "rect":
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        return x, y, x + float(el.get("width", 0)), y + float(el.get("height", 0))
    elif t == "path":
        v = list(map(float, NUM.findall(el.get("d", ""))))
        xs, ys = v[0::2], v[1::2]
    else:
        return None
    if not xs or not ys:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def node_text(g):
    lines = []
    for t in g.iter("text"):
        s = "".join(t.itertext()).strip()
        if s:
            lines.append(s)
    return "\n".join(lines)


def split_edge_title(title):
    m = re.match(r"^(.*?)\s*(->|--)\s*(.*)$", title)
    if not m:
        return None
    return m.group(1), m.group(3), m.group(2) == "->"


def parse_graphviz(root):
    nodes, edges, clusters = {}, [], []
    for g in root.iter("g"):
        cls = (g.get("class") or "").split()
        if not cls:
            continue
        title_el = g.find("title")
        title = (title_el.text or "").strip() if title_el is not None else ""
        if "node" in cls:
            shapes = [b for b in (shape_bbox(e) for e in g
                                  if e.tag in ("polygon", "ellipse", "rect", "path", "polyline")) if b]
            if not shapes:
                continue
            first = next(e for e in g if e.tag in ("polygon", "ellipse", "rect", "path"))
            b = shapes[0]
            nodes[title] = dict(
                x=b[0], y=b[1], w=b[2] - b[0], h=b[3] - b[1],
                text=node_text(g) or title,
                fill=(first.get("fill") or "").lower(),
            )
        elif "edge" in cls:
            r = split_edge_title(title)
            if r:
                edges.append(dict(src=r[0], dst=r[1], directed=r[2], label=node_text(g)))
        elif "cluster" in cls:
            poly = next((e for e in g if e.tag in ("polygon", "rect", "path")), None)
            b = shape_bbox(poly) if poly is not None else None
            if b:
                clusters.append(dict(label=node_text(g) or title, box=b))
    def resolve(name):  # quita el puerto (nodo:puerto) solo si hace falta
        while name not in nodes and ":" in name:
            name = name.rsplit(":", 1)[0]
        return name
    for e in edges:
        e["src"], e["dst"] = resolve(e["src"]), resolve(e["dst"])
    edges = [e for e in edges if e["src"] in nodes and e["dst"] in nodes]
    return nodes, edges, clusters


def parse_generic(root):
    """Respaldo para SVG no-Graphviz: un nodo por cada <text>."""
    nodes = {}

    def walk(el, tx, ty):
        m = re.search(r"translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)", el.get("transform", "") or "")
        if m:
            tx, ty = tx + float(m.group(1)), ty + float(m.group(2))
        if el.tag == "text":
            s = "".join(el.itertext()).strip()
            if s:
                nodes[f"t{len(nodes)}"] = dict(
                    x=float(el.get("x", 0) or 0) + tx, y=float(el.get("y", 0) or 0) + ty,
                    w=0, h=0, text=s, fill="")
        for c in el:
            walk(c, tx, ty)
    walk(root, 0, 0)
    return nodes, [], []


# ─────────────────────────────── layout ───────────────────────────────────
def size_for(text):
    lines = text.split("\n")
    w = max(len(l) for l in lines) * 10 + 48
    return max(200, min(w, 520)), max(56, 28 * len(lines) + 28)


def spanning_forest(nodes, edges, order_key):
    children = {k: [] for k in nodes}
    indeg = {k: 0 for k in nodes}
    for e in edges:
        indeg[e["dst"]] += 1
    seen, tree_edges = set(), set()

    def dfs(n):
        seen.add(n)
        for e in sorted((e for e in edges if e["src"] == n), key=lambda e: order_key(nodes[e["dst"]])):
            if e["dst"] not in seen:
                children[n].append(e["dst"])
                tree_edges.add((e["src"], e["dst"]))
                dfs(e["dst"])

    roots = sorted((k for k in nodes if indeg[k] == 0), key=lambda k: order_key(nodes[k]))
    for r in roots + sorted(nodes, key=lambda k: order_key(nodes[k])):
        if r not in seen:
            if r not in roots:
                roots.append(r)
            dfs(r)
    return roots, children, tree_edges


def is_forest(nodes, edges, tree_edges):
    indeg = {}
    for e in edges:
        indeg[e["dst"]] = indeg.get(e["dst"], 0) + 1
    return all(v == 1 for v in indeg.values()) and len(tree_edges) == len(edges)


def layout_tree(nodes, roots, children, horizontal):
    GAP_MAIN, GAP_CROSS = 70, 28
    sizes = {k: size_for(v["text"]) for k, v in nodes.items()}
    pos, cursor = {}, [0]

    def cross(n):  # tamaño en el eje transversal
        return sizes[n][1] if horizontal else sizes[n][0]

    def place(n, depth_off):
        kids = children[n]
        if not kids:
            c = cursor[0] + cross(n) / 2
            cursor[0] += cross(n) + GAP_CROSS
        else:
            cs = [place(k, 0) for k in kids]
            c = (cs[0] + cs[-1]) / 2
        pos[n] = c
        return c

    # profundidad -> offset acumulado según el ancho máximo de cada nivel
    depth = {}

    def set_depth(n, d):
        depth[n] = d
        for k in children[n]:
            set_depth(k, d + 1)
    for r in roots:
        set_depth(r, 0)
        place(r, 0)
        cursor[0] += GAP_CROSS
    main_size = {}
    for n, d in depth.items():
        s = sizes[n][0] if horizontal else sizes[n][1]
        main_size[d] = max(main_size.get(d, 0), s)
    offs, acc = {}, 0
    for d in sorted(main_size):
        offs[d] = acc
        acc += main_size[d] + GAP_MAIN
    out = {}
    for n in nodes:
        w, h = sizes[n]
        if horizontal:
            out[n] = (offs[depth[n]], pos[n] - h / 2, w, h)
        else:
            out[n] = (pos[n] - w / 2, offs[depth[n]], w, h)
    return out


def layout_original(nodes):
    sizes = {k: size_for(v["text"]) for k, v in nodes.items()}
    cx = {k: v["x"] + v["w"] / 2 for k, v in nodes.items()}
    cy = {k: v["y"] + v["h"] / 2 for k, v in nodes.items()}
    keys = list(nodes)

    def overlaps(s):
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if (abs(cx[a] - cx[b]) * s < (sizes[a][0] + sizes[b][0]) / 2 + 20 and
                        abs(cy[a] - cy[b]) * s < (sizes[a][1] + sizes[b][1]) / 2 + 20):
                    return True
        return False
    s = 1.0
    while overlaps(s) and s < 12:
        s *= 1.15
    return {k: (cx[k] * s - sizes[k][0] / 2, cy[k] * s - sizes[k][1] / 2, *sizes[k]) for k in keys}, s


# ─────────────────────────────── canvas ───────────────────────────────────
def uid(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]


def pick_sides(a, b, mode):
    if mode == "tree-lr":
        return "right", "left"
    if mode == "tree-td":
        return "bottom", "top"
    ax, ay = a[0] + a[2] / 2, a[1] + a[3] / 2
    bx, by = b[0] + b[2] / 2, b[1] + b[3] / 2
    if abs(bx - ax) * 0.6 > abs(by - ay):
        return ("right", "left") if bx > ax else ("left", "right")
    return ("bottom", "top") if by > ay else ("top", "bottom")


def convert(svg_path, layout="auto", color=True, groups=True):
    root = strip_ns(ET.parse(svg_path).getroot())
    nodes, edges, clusters = parse_graphviz(root)
    generic = not nodes
    if generic:
        nodes, edges, clusters = parse_generic(root)
        if not nodes:
            raise SystemExit("No se encontraron nodos ni textos en el SVG.")
        print("Aviso: no parece un SVG de Graphviz; modo de respaldo (solo textos).", file=sys.stderr)
        layout = "original"

    # Orden de hermanos según la orientación dominante del grafo
    dx = sum(abs(nodes[e["dst"]]["x"] - nodes[e["src"]]["x"]) for e in edges)
    dy = sum(abs(nodes[e["dst"]]["y"] - nodes[e["src"]]["y"]) for e in edges)
    key = (lambda n: n["x"]) if dy >= dx else (lambda n: n["y"])

    roots, children, tree_edges = spanning_forest(nodes, edges, key) if edges else ([], {}, set())
    mode = layout
    if mode == "auto":
        mode = "tree-lr" if edges and is_forest(nodes, edges, tree_edges) else "original"
    if mode.startswith("tree") and not edges:
        mode = "original"

    scale = 1.0
    if mode == "original":
        boxes, scale = layout_original(nodes)
    else:
        boxes = layout_tree(nodes, roots, children, horizontal=(mode == "tree-lr"))

    cn, ce = [], []
    for k, v in nodes.items():
        x, y, w, h = boxes[k]
        n = dict(id=uid("n" + k), type="text", text=v["text"],
                 x=int(x), y=int(y), width=int(w), height=int(h))
        f = v["fill"]
        if color and f not in LIGHT and f != "#eeeeee":
            if re.fullmatch(r"#[0-9a-f]{6}", f):
                n["color"] = f
        cn.append(n)
    for e in edges:
        s, t = pick_sides(boxes[e["src"]], boxes[e["dst"]], mode)
        d = dict(id=uid(f"e{e['src']}>{e['dst']}"), fromNode=uid("n" + e["src"]), fromSide=s,
                 toNode=uid("n" + e["dst"]), toSide=t)
        if not e["directed"]:
            d["toEnd"] = "none"
        if e["label"]:
            d["label"] = e["label"]
        ce.append(d)

    # clusters -> grupos (solo en layout original, donde las posiciones se conservan)
    if groups and clusters and mode == "original":
        for c in clusters:
            x0, y0, x1, y1 = c["box"]
            cn.insert(0, dict(id=uid("g" + c["label"] + str(x0)), type="group", label=c["label"],
                              x=int(x0 * scale) - 20, y=int(y0 * scale) - 20,
                              width=int((x1 - x0) * scale) + 40, height=int((y1 - y0) * scale) + 40))
    return dict(nodes=cn, edges=ce), mode


def main():
    ap = argparse.ArgumentParser(description="Convierte un SVG de Graphviz en un .canvas de Obsidian.")
    ap.add_argument("svg")
    ap.add_argument("-o", "--output")
    ap.add_argument("--layout", choices=["auto", "tree-lr", "tree-td", "original"], default="auto")
    ap.add_argument("--no-color", action="store_true", help="no copiar los colores de relleno")
    ap.add_argument("--no-groups", action="store_true", help="no convertir clusters en grupos")
    a = ap.parse_args()
    data, mode = convert(a.svg, a.layout, not a.no_color, not a.no_groups)
    out = Path(a.output) if a.output else Path(a.svg).with_suffix(".canvas")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{out}: {len(data['nodes'])} nodos, {len(data['edges'])} conexiones (layout: {mode})")


if __name__ == "__main__":
    main()
