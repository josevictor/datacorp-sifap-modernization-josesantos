#!/usr/bin/env python3
"""
add-shape.py: adiciona uma nova forma de vértice a um arquivo de diagrama .drawio existente.

Uso:
    python scripts/add-shape.py <diagram.drawio> <label> <x> <y> [options]

Exemplos:
    python scripts/add-shape.py docs/flowchart.drawio "Nova etapa" 400 300
    python scripts/add-shape.py docs/arch.drawio "Decisão" 400 400 \\
        --width 160 --height 80 \\
        --style "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
    python scripts/add-shape.py docs/arch.drawio "Visualizar nó" 200 200 --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path


DEFAULT_STYLE = "rounded=1;whiteSpace=wrap;html=1;"


def _indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Recua a árvore XML no local. Substitui ET.indent() para compatibilidade com Python 3.8."""
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_xml(child, level + 1)
        # cauda do último filho
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent
    if not level:
        elem.tail = "\n"


def _generate_id(label: str, x: int, y: int) -> str:
    """Gera um ID curto quase determinístico com base em rótulo + posição + tempo."""
    seed = f"{label}:{x}:{y}:{time.time_ns()}"
    return "auto_" + hashlib.sha1(seed.encode()).hexdigest()[:8]


def add_shape(
    path: Path,
    label: str,
    x: int,
    y: int,
    width: int = 120,
    height: int = 60,
    style: str = DEFAULT_STYLE,
    diagram_index: int = 0,
    dry_run: bool = False,
) -> int:
    """
    Analisa o arquivo .drawio, insere uma nova célula de vértice na página
    especificada do diagrama e grava o arquivo (salvo quando dry_run for True).

    Retorna:
        0 em caso de sucesso, 1 em caso de falha.
    """
    # Preserva a declaração XML / indentação original ao gravar bytes brutos.
    ET.register_namespace("", "")

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        print(f"ERRO: erro de análise XML em '{path}': {exc}")
        return 1

    mxfile = tree.getroot()
    if mxfile.tag != "mxfile":
        print(f"ERRO: o elemento-raiz deve ser <mxfile>, recebido <{mxfile.tag}>")
        return 1

    diagrams = mxfile.findall("diagram")
    if diagram_index >= len(diagrams):
        print(
            f"ERRO: diagram-index {diagram_index} está fora do intervalo "
            f"(o arquivo tem {len(diagrams)} diagrama(s))"
        )
        return 1

    diagram = diagrams[diagram_index]
    graph_model = diagram.find("mxGraphModel")
    if graph_model is None:
        print(
            "ERRO: <mxGraphModel> não foi encontrado como filho direto. "
            "Diagramas compactados não são compatíveis."
        )
        return 1

    root_elem = graph_model.find("root")
    if root_elem is None:
        print("ERRO: elemento <root> não encontrado dentro de <mxGraphModel>")
        return 1

    # Determina o ID do pai, com padrão "1" (a camada-padrão)
    parent_id = "1"
    existing_ids = {c.get("id") for c in root_elem.findall("mxCell") if c.get("id")}
    if parent_id not in existing_ids:
        # Usa como alternativa o primeiro ID de célula diferente de "0"
        for c in root_elem.findall("mxCell"):
            cid = c.get("id")
            if cid and cid != "0":
                parent_id = cid
                break

    # Gera um ID exclusivo
    new_id = _generate_id(label, x, y)
    while new_id in existing_ids:
        new_id = _generate_id(label + "_", x, y)

    # Cria o novo elemento mxCell
    new_cell = ET.Element("mxCell")
    new_cell.set("id", new_id)
    new_cell.set("value", label)
    new_cell.set("style", style)
    new_cell.set("vertex", "1")
    new_cell.set("parent", parent_id)

    geom = ET.SubElement(new_cell, "mxGeometry")
    geom.set("x", str(x))
    geom.set("y", str(y))
    geom.set("width", str(width))
    geom.set("height", str(height))
    geom.set("as", "geometry")

    if dry_run:
        print("SIMULAÇÃO: XML da nova célula (não gravado):")
        print(ET.tostring(new_cell, encoding="unicode"))
        print(f"\nAdicionaria ao diagrama '{diagram.get('name', diagram_index)}' em '{path}'")
        return 0

    root_elem.append(new_cell)

    # Grava preservando a declaração XML (usa _indent_xml para compatibilidade com Python 3.8)
    _indent_xml(tree.getroot())
    tree.write(str(path), encoding="utf-8", xml_declaration=True)

    print(
        f"Forma id=\"{new_id}\" adicionada à página {diagram_index} "
        f"('{diagram.get('name', '')}') de {path}"
    )
    return 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adiciona uma forma a um arquivo de diagrama .drawio existente.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("diagram", help="Caminho do arquivo .drawio")
    parser.add_argument("label", help="Rótulo de texto da nova forma")
    parser.add_argument("x", type=int, help="Coordenada X (pixels)")
    parser.add_argument("y", type=int, help="Coordenada Y (pixels)")
    parser.add_argument("--width", type=int, default=120, help="Largura da forma (padrão: 120)")
    parser.add_argument("--height", type=int, default=60, help="Altura da forma (padrão: 60)")
    parser.add_argument(
        "--style",
        default=DEFAULT_STYLE,
        help=f'string de estilo do draw.io (padrão: "{DEFAULT_STYLE}")',
    )
    parser.add_argument(
        "--diagram-index",
        type=int,
        default=0,
        help="Índice, com base zero, da página do diagrama que receberá a forma (padrão: 0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Imprime o XML da nova célula sem gravar no arquivo",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    path = Path(args.diagram)

    if not path.exists():
        print(f"ERRO: arquivo não encontrado: {path}")
        return 1
    if not path.is_file():
        print(f"ERRO: não é um arquivo: {path}")
        return 1

    return add_shape(
        path=path,
        label=args.label,
        x=args.x,
        y=args.y,
        width=args.width,
        height=args.height,
        style=args.style,
        diagram_index=args.diagram_index,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
