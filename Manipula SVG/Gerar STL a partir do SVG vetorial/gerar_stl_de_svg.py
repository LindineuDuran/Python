import os
import sys
import trimesh
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from svgpathtools import parse_path
from xml.etree import ElementTree as ET

# ---------- CONFIGURAÇÃO ----------
APP_PATH = r'D:\GitHub\Python\Manipula SVG\Gerar STL a partir do SVG vetorial'
ARQUIVO_SVG = os.path.join(APP_PATH, 'Bob_Marley.svg')
ARQUIVO_STL = os.path.join(APP_PATH, 'Bob Marley.stl')

EXTRUDE_HEIGHT = 5.0      # mm
SAMPLES_PER_UNIT = 2.5    # pontos por unidade de comprimento (aumente para mais resolução)
MIN_SAMPLES_PER_SEG = 3   # mínimo de amostras por segmento
TOL = 1e-6
FLIP_Y = True             # Inkscape Y cresce pra baixo; defina False se você não quiser inverter
# -----------------------------------

# --- Checar motor de triangulação ---
try:
    import mapbox_earcut
    TRI_ENGINE = "earcut"
except ImportError:
    print("Aviso: mapbox_earcut não encontrado. Instale com: pip install mapbox-earcut")
    TRI_ENGINE = None

def sample_segment(seg, samples_per_unit=SAMPLES_PER_UNIT, min_samples=MIN_SAMPLES_PER_SEG):
    """Amostra um segmento em parâmetro t ∈ [0,1]. Retorna lista de (x,y)."""
    try:
        seg_len = seg.length()
    except Exception:
        seg_len = 0.0
    n = max(min_samples, int(max(1.0, seg_len) * samples_per_unit))
    pts = []
    for i in range(n):
        t = i / float(n)
        p = seg.point(t)
        pts.append((p.real, p.imag))
    pts.append((seg.point(1.0).real, seg.point(1.0).imag))
    return pts

def path_to_subpolygons(d):
    """Recebe um atributo 'd' e retorna lista de subpolygons (cada um é lista de (x,y))."""
    try:
        path = parse_path(d)
    except Exception:
        return []
    subpolys = []
    current = []

    for seg in path:
        cls = seg.__class__.__name__
        if cls == "Move":
            if current:
                subpolys.append(current)
            current = [(seg.end.real, seg.end.imag)]
            continue

        pts = sample_segment(seg)
        for (x, y) in pts:
            if not current:
                current.append((x, y))
            else:
                lx, ly = current[-1]
                if (abs(lx - x) > TOL) or (abs(ly - y) > TOL):
                    current.append((x, y))

    if current:
        subpolys.append(current)

    # fechar subpolygons automaticamente
    fixed = []
    for coords in subpolys:
        if len(coords) >= 3:
            x0, y0 = coords[0]
            xn, yn = coords[-1]
            if abs(x0 - xn) < 1e-3 and abs(y0 - yn) < 1e-3:
                coords[-1] = coords[0]
        fixed.append(coords)
    return fixed

def coords_to_polygon(coords, flip_y=FLIP_Y):
    if flip_y:
        coords2 = [(x, -y) for (x, y) in coords]
    else:
        coords2 = coords[:]
    try:
        poly = Polygon(coords2)
    except Exception:
        return None
    if not poly.is_valid:
        poly = poly.buffer(0)
    if not poly.is_valid or poly.is_empty:
        return None
    return poly

def svg_paths_from_file(svg_filepath):
    tree = ET.parse(svg_filepath)
    root = tree.getroot()
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0].strip("{")
    tag = f".//{{{ns}}}path" if ns else ".//path"
    elems = root.findall(tag)
    ds = []
    for e in elems:
        d = e.get("d")
        if d:
            ds.append(d)
    return ds

def generate_stl_from_svg(svg_path, stl_path, extrude_height=EXTRUDE_HEIGHT):
    if TRI_ENGINE is None:
        raise RuntimeError("Nenhum motor de triangulação disponível. Instale mapbox-earcut.")
    
    ds = svg_paths_from_file(svg_path)
    polys = []

    for d in ds:
        subpolys = path_to_subpolygons(d)
        for coords in subpolys:
            if len(coords) < 3:
                continue
            poly = coords_to_polygon(coords)
            if poly is None:
                continue
            polys.append(poly)

    if not polys:
        raise RuntimeError("Nenhum polígono válido gerado a partir do SVG (verifique paths).")

    geom = unary_union(polys)

    # extrudir com engine explícita
    if isinstance(geom, Polygon):
        mesh = trimesh.creation.extrude_polygon(geom, extrude_height, triangulate_kwargs={"engine": TRI_ENGINE})
    elif isinstance(geom, MultiPolygon):
        meshes = []
        for p in geom.geoms:
            meshes.append(trimesh.creation.extrude_polygon(p, extrude_height, triangulate_kwargs={"engine": TRI_ENGINE}))
        mesh = trimesh.util.concatenate(meshes)
    else:
        raise RuntimeError("Geometria resultante inesperada: " + str(type(geom)))

    mesh.export(stl_path)
    return stl_path

if __name__ == "__main__":
    print("Lendo SVG:", ARQUIVO_SVG)
    try:
        out = generate_stl_from_svg(ARQUIVO_SVG, ARQUIVO_STL, EXTRUDE_HEIGHT)
        print("STL gerado:", out)
    except Exception as e:
        print("Erro:", e)
        sys.exit(1)