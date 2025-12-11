import os
from svgpathtools import svg2paths2, wsvg, parse_path
from copy import deepcopy
import csv

# 🔧 CONFIGURAÇÕES:
app_path = 'c:/Users/LindineuDuran/Downloads/Desenho 3D/'
ARQUIVO_SVG = os.path.join(app_path, 'Bob Marley plano.svg')
ARQUIVO_SVG_ABERTOS = os.path.join(app_path, 'Bob Marley plano_abertos.svg')
ARQUIVO_SVG_FECHADOS = os.path.join(app_path, 'Bob Marley plano_fechados.svg')
ARQUIVO_CSV_ABERTOS = os.path.join(app_path, 'caminhos_abertos.csv')


# << Se False, o SVG "abertos" também incluirá os fechados sem destaque
EXPORTAR_SOMENTE_ABERTOS = True

# Raio do círculo que marca visualmente os pontos abertos
RAIO_MARCA = 3


def is_path_closed(path):
    """Verifica se o caminho é fechado comparando início e fim (com pequena tolerância)."""
    if not path:
        return True
    start = path[0].start
    end = path[-1].end
    return abs(start - end) < 1e-6


def extrair_pontos(path):
    """Extrai todos os pontos (x,y) visitados (início de cada segmento + ponto final)."""
    pontos = []
    for segment in path:
        pontos.append((segment.start.real, segment.start.imag))
    # adiciona o último ponto final
    pontos.append((path[-1].end.real, path[-1].end.imag))
    return pontos


def make_circle_path(cx, cy, r):
    """
    Cria um círculo como Path usando dois arcos.
    Usa comando relativo 'a' para simplificar.
    """
    d = (
        f"M {cx - r},{cy} "
        f"a {r},{r} 0 1,0 {2*r},0 "
        f"a {r},{r} 0 1,0 {-2*r},0 z"
    )
    return parse_path(d)


def verificar_e_exportar_caminhos(arquivo_entrada,
                                  arquivo_saida_abertos,
                                  arquivo_saida_fechados,
                                  arquivo_csv_abertos,
                                  somente_abertos=False):
    paths, attributes, svg_attributes = svg2paths2(arquivo_entrada)

    caminhos_abertos = []
    novos_paths_abertos = []
    novos_atributos_abertos = []
    novos_paths_fechados = []
    novos_atributos_fechados = []

    for i, path in enumerate(paths):
        id_path = attributes[i].get('id', f'path_{i}')
        d_atributo = attributes[i].get("d", "")

        pontos = extrair_pontos(path)
        start_point = path[0].start
        end_point = path[-1].end

        if not is_path_closed(path):
            # Indica quais pontas estão "abertas" (em caminho aberto, início ≠ fim)
            ponto_aberto = []
            if abs(start_point - end_point) > 1e-6:
                ponto_aberto.extend(["start_point", "end_point"])

                # Guarda info para CSV
                caminhos_abertos.append({
                    "index": i,
                    "id": id_path,
                    "start_point": f"{start_point.real},{start_point.imag}",
                    "end_point": f"{end_point.real},{end_point.imag}",
                    "ponto_aberto": " e ".join(ponto_aberto),
                    "pontos": " | ".join([f"{x},{y}" for x, y in pontos]),
                    "d": d_atributo
                })

                # Adiciona caminho aberto com destaque
                attr_path = deepcopy(attributes[i])
                attr_path['style'] = 'stroke:#ff0000; stroke-width:2; fill:none'
                novos_paths_abertos.append(path)
                novos_atributos_abertos.append(attr_path)

                # Marca visualmente os pontos de início e fim com círculos (como Path)
                for label, p in (("start", start_point), ("end", end_point)):
                    circle_path = make_circle_path(p.real, p.imag, RAIO_MARCA)
                    novos_paths_abertos.append(circle_path)
                    novos_atributos_abertos.append({
                        'style': 'fill:#ff0000; stroke:none',
                        'id': f"marca_{label}_{id_path}_{p.real:.2f}_{p.imag:.2f}"
                    })

        else:
            # Caminhos fechados
            novos_paths_fechados.append(path)
            novos_atributos_fechados.append(deepcopy(attributes[i]))

            # Se desejado, incluir também no SVG "abertos" (sem destaque)
            if not somente_abertos:
                novos_paths_abertos.append(path)
                novos_atributos_abertos.append(deepcopy(attributes[i]))

    # Salvar SVG com abertos (e possivelmente fechados)
    if novos_paths_abertos:
        wsvg(novos_paths_abertos, attributes=novos_atributos_abertos,
             svg_attributes=svg_attributes, filename=arquivo_saida_abertos)
    else:
        print("ℹ️ Nenhum caminho para salvar no SVG de abertos; arquivo não foi gerado.")

    # Salvar SVG só com fechados
    if novos_paths_fechados:
        wsvg(novos_paths_fechados, attributes=novos_atributos_fechados,
             svg_attributes=svg_attributes, filename=arquivo_saida_fechados)
    else:
        print("ℹ️ Nenhum caminho fechado para salvar; arquivo de fechados não foi gerado.")

    # Exportar CSV com caminhos abertos
    if caminhos_abertos:
        with open(arquivo_csv_abertos, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=["index", "id", "start_point", "end_point", "ponto_aberto", "pontos", "d"]
            )
            writer.writeheader()
            writer.writerows(caminhos_abertos)

        print(f"\n❌ {len(caminhos_abertos)} caminho(s) aberto(s) encontrado(s).")
        print(f"🖍️ Caminhos abertos exportados no SVG: {arquivo_saida_abertos}")
        print(f"📦 Caminhos abertos salvos em CSV: {arquivo_csv_abertos}")
    else:
        print("\n✅ Todos os caminhos estão fechados! (CSV de abertos não gerado.)")

    if novos_paths_fechados:
        print(f"🟢 Caminhos fechados exportados no SVG: {arquivo_saida_fechados}")


if __name__ == "__main__":
    verificar_e_exportar_caminhos(
        ARQUIVO_SVG,
        ARQUIVO_SVG_ABERTOS,
        ARQUIVO_SVG_FECHADOS,
        ARQUIVO_CSV_ABERTOS,
        somente_abertos=EXPORTAR_SOMENTE_ABERTOS
    )