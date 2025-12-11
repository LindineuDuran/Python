import os
from svgpathtools import parse_path
from copy import deepcopy
import xml.etree.ElementTree as ET
import csv

# 🔧 CONFIGURAÇÕES:
app_path = 'c:/Users/LindineuDuran/Downloads/Desenho 3D/'
ARQUIVO_SVG = os.path.join(app_path, 'Bob Marley plano.svg')
ARQUIVO_SVG_ABERTOS = os.path.join(app_path, 'Bob Marley plano_abertos.svg')
ARQUIVO_SVG_FECHADOS = os.path.join(app_path, 'Bob Marley plano_fechados.svg')
ARQUIVO_CSV_ABERTOS = os.path.join(app_path, 'caminhos_abertos.csv')
RAIO_MARCA = 2
TOLERANCIA = 1e-3  # tolerância para considerar pontos iguais


def get_svg_namespace(root):
    """Retorna a namespace do SVG (ex: 'http://www.w3.org/2000/svg')."""
    if root.tag.startswith("{"):
        return root.tag.split("}")[0].strip("{")
    return "http://www.w3.org/2000/svg"


def make_circle_element(ns, cx, cy, r, mid):
    """Cria um elemento <circle> no namespace ns para marcar pontos."""
    tag = f"{{{ns}}}circle"
    el = ET.Element(tag)
    el.set("cx", f"{cx:.3f}")
    el.set("cy", f"{cy:.3f}")
    el.set("r", str(r))
    el.set("style", "fill:#ff0000; stroke:none")
    el.set("id", mid)
    return el


def safe_parse_path(d):
    """Tenta parsear o d; retorna None se falhar."""
    try:
        return parse_path(d)
    except Exception:
        return None


def analisar_e_corrigir(arquivo_svg, arquivo_abertos, arquivo_fechados, arquivo_csv):
    tree = ET.parse(arquivo_svg)
    root = tree.getroot()
    ns = get_svg_namespace(root)
    path_tag = f".//{{{ns}}}path"

    path_elems = root.findall(path_tag)

    report = []  # para CSV: dicts com dados por path
    abertos_e_marcadores = []  # (elem_copy, [circles])

    # iterar e corrigir no XML tree (in-place)
    for idx, elem in enumerate(path_elems):
        d_original = (elem.get("d") or "").strip()
        elem_id = elem.get("id", f"path{idx}")

        parsed = safe_parse_path(d_original)
        if parsed is None:
            # não conseguimos parsear (pular, registrar)
            report.append({
                "index": idx,
                "id": elem_id,
                "sobreposto": "",
                "tem_Z": ("Z" in d_original or "z" in d_original),
                "start": "",
                "end": "",
                "d_original": d_original,
                "d_corrigido": "",
                "corrigido": "parse_fail"
            })
            continue

        start = parsed[0].start
        end = parsed[-1].end
        sobreposto = abs(start - end) < TOLERANCIA
        tem_Z = ("z" in d_original) or ("Z" in d_original)

        d_corrigido = d_original  # por padrão
        corrigiu = False

        # caso 1: nós sobrepostos (start ~ end) mas sem Z -> inserir Z
        if sobreposto and not tem_Z:
            # adiciona um espaço e Z
            d_corrigido = d_original + " Z"
            elem.set("d", d_corrigido)
            corrigiu = True

        # caso 2: realmente aberto (start != end) e sem Z -> adicionar L startx,starty Z
        elif (not sobreposto) and (not tem_Z):
            # pedimos uma linha até o ponto inicial (com coordenadas absolutas)
            sx, sy = start.real, start.imag
            # garantimos um espaço entre comandos
            d_corrigido = d_original + f" L {sx:.3f},{sy:.3f} Z"
            elem.set("d", d_corrigido)
            corrigiu = True

        # recalc parse do d_corrigido para obter start/end atualizados (segurança)
        parsed_corr = safe_parse_path(d_corrigido)
        if parsed_corr is not None:
            start_corr = parsed_corr[0].start
            end_corr = parsed_corr[-1].end
        else:
            start_corr = start
            end_corr = end

        # se originalmente estava aberto (antes da correção), guardamos para SVG de abertos e marcadores
        originally_open = (not tem_Z and (sobreposto or (abs(start - end) > TOLERANCIA)))

        circles = []
        if originally_open:
            # marca visual nos pontos problemáticos (usamos as coordenadas originais start/end)
            circles.append(make_circle_element(ns, start.real, start.imag, RAIO_MARCA, f"marca_{elem_id}_start"))
            circles.append(make_circle_element(ns, end.real, end.imag, RAIO_MARCA, f"marca_{elem_id}_end"))
            # guardamos uma cópia do elemento (com d_corrigido ou original?) -> vamos copiar o estado atual do elem
            abertos_e_marcadores.append((deepcopy(elem), circles))

        report.append({
            "index": idx,
            "id": elem_id,
            "sobreposto": sobreposto,
            "tem_Z": tem_Z,
            "start": f"{start.real:.3f},{start.imag:.3f}",
            "end": f"{end.real:.3f},{end.imag:.3f}",
            "d_original": d_original,
            "d_corrigido": d_corrigido if corrigiu else "",
            "corrigido": "yes" if corrigiu else "no"
        })

    # 1) Escrever SVG corrigido (root já foi modificado in-place)
    tree.write(arquivo_fechados, encoding="utf-8", xml_declaration=True)

    # 2) Criar SVG contendo apenas os abertos + marcadores
    # copiamos o elemento root (preservando atributos do SVG)
    new_root = ET.Element(root.tag, root.attrib)
    # opcional: copiar defs se existirem (para estilos). Vamos tentar copiar <defs> se houver
    defs = root.find(f".//{{{ns}}}defs")
    if defs is not None:
        new_root.append(deepcopy(defs))

    # adicionar cada path aberto (e seus marcadores)
    for elem_copy, circles in abertos_e_marcadores:
        new_root.append(elem_copy)
        for c in circles:
            new_root.append(c)

    # salvar o SVG de abertos (se houver)
    if len(abertos_e_marcadores) > 0:
        tree_abertos = ET.ElementTree(new_root)
        tree_abertos.write(arquivo_abertos, encoding="utf-8", xml_declaration=True)
    else:
        # criar um SVG vazio com mesmas dimensões (opcional) — aqui preferimos não criar arquivo se não há abertos
        pass

    # 3) Escrever CSV com relatório
    with open(arquivo_csv, "w", newline="", encoding="utf-8") as fcsv:
        campos = ["index", "id", "sobreposto", "tem_Z", "start", "end", "d_original", "d_corrigido", "corrigido"]
        writer = csv.DictWriter(fcsv, fieldnames=campos)
        writer.writeheader()
        for r in report:
            writer.writerow(r)

    # resumo impresso
    total = len(report)
    abertos_count = sum(1 for r in report if (r["corrigido"] == "yes" or (r["tem_Z"] == False and (r["sobreposto"] or r["d_original"] == ""))))
    print(f"Processados {total} paths. Corrigidos / marcados: {abertos_count}.")
    print(f"SVG corrigido gravado em: {arquivo_fechados}")
    if len(abertos_e_marcadores) > 0:
        print(f"SVG com abertos e marcas gravado em: {arquivo_abertos}")
    print(f"CSV relatório gravado em: {arquivo_csv}")


if __name__ == "__main__":
    analisar_e_corrigir(ARQUIVO_SVG, ARQUIVO_SVG_ABERTOS, ARQUIVO_SVG_FECHADOS, ARQUIVO_CSV_ABERTOS)
