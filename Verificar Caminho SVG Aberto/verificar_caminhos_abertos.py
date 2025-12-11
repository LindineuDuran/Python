from svgpathtools import svg2paths2, wsvg
from copy import deepcopy
import csv

# 🔧 CONFIGURAÇÕES:
ARQUIVO_SVG = "Bob Marley plano.svg"
ARQUIVO_SVG_ABERTOS = "Bob Marley plano_abertos.svg"
ARQUIVO_SVG_FECHADOS = "Bob Marley plano_fechados.svg"
ARQUIVO_CSV = "Bob Marley plano_abertos.csv"


def is_path_closed(path):
    """Verifica se o caminho é fechado comparando início e fim."""
    if not path:
        return True
    start = path[0].start
    end = path[-1].end
    return abs(start - end) < 1e-6


def verificar_salvar_dividido_exportar_csv(arquivo_svg, svg_abertos, svg_fechados, csv_saida):
    paths, attributes, svg_attributes = svg2paths2(arquivo_svg)

    caminhos_abertos = []
    caminhos_fechados = []

    paths_abertos = []
    atributos_abertos = []

    paths_fechados = []
    atributos_fechados = []

    for i, path in enumerate(paths):
        id_path = attributes[i].get('id', f'path_{i}')
        attr = deepcopy(attributes[i])

        if not is_path_closed(path):
            start = path[0].start
            end = path[-1].end

            caminhos_abertos.append({
                'index': i,
                'id': id_path,
                'start': f"{start.real:.2f},{start.imag:.2f}",
                'end': f"{end.real:.2f},{end.imag:.2f}"
            })

            attr['style'] = 'stroke:#ff0000; stroke-width:2; fill:none'
            paths_abertos.append(path)
            atributos_abertos.append(attr)

        else:
            caminhos_fechados.append((i, id_path))
            paths_fechados.append(path)
            atributos_fechados.append(attr)

    # Salvar SVGs separados
    wsvg(paths_abertos, attributes=atributos_abertos,
         svg_attributes=svg_attributes, filename=svg_abertos)

    wsvg(paths_fechados, attributes=atributos_fechados,
         svg_attributes=svg_attributes, filename=svg_fechados)

    # Exportar CSV
    if caminhos_abertos:
        with open(csv_saida, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['index', 'id', 'start_point', 'end_point']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in caminhos_abertos:
                writer.writerow({
                    'index': item['index'],
                    'id': item['id'],
                    'start_point': item['start'],
                    'end_point': item['end']
                })

    # Mensagens no terminal
    print(f"\n✅ Total de caminhos processados: {len(paths)}")
    print(f"🔴 Caminhos abertos: {len(caminhos_abertos)}")
    print(f"✅ Caminhos fechados: {len(caminhos_fechados)}")

    if caminhos_abertos:
        print(f"\n🖍️ Caminhos abertos salvos em: {svg_abertos}")
        print(f"📄 Detalhes exportados em CSV: {csv_saida}")
    print(f"\n🟢 Caminhos fechados salvos em: {svg_fechados}")


if __name__ == "__main__":
    verificar_salvar_dividido_exportar_csv(
        ARQUIVO_SVG,
        ARQUIVO_SVG_ABERTOS,
        ARQUIVO_SVG_FECHADOS,
        ARQUIVO_CSV
    )
