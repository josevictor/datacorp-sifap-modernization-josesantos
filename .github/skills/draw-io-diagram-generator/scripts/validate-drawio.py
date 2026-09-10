#!/usr/bin/env python3
"""
validate-drawio.py: valida a estrutura XML de um arquivo de diagrama .drawio.

Uso:
    python scripts/validate-drawio.py <path-to-file.drawio>

Códigos de saída:
    0  Todas as verificações passaram
    1  Um ou mais erros de validação encontrados
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _error(msg: str, errors: list) -> None:
    errors.append(msg)
    print(f"  ERRO: {msg}")


def validate_file(path: Path) -> list[str]:
    """Analisa e valida um único arquivo .drawio. Retorna uma lista de strings de erro."""
    errors: list[str] = []

    # --- Boa formação do XML ---
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"Erro de análise XML: {exc}"]

    root = tree.getroot()
    if root.tag != "mxfile":
        _error(f"O elemento-raiz deve ser <mxfile>, recebido <{root.tag}>", errors)
        return errors

    diagrams = root.findall("diagram")
    if not diagrams:
        _error("Nenhum elemento <diagram> encontrado dentro de <mxfile>", errors)
        return errors

    for d_idx, diagram in enumerate(diagrams):
        d_name = diagram.get("name", f"página-{d_idx}")
        prefix = f"[diagrama '{d_name}']"

        # Localiza mxGraphModel (pode ser filho direto ou codificado em base64; tratamos somente o direto)
        graph_model = diagram.find("mxGraphModel")
        if graph_model is None:
            print(f"  IGNORADO {prefix}: mxGraphModel não encontrado como filho direto (pode estar compactado)")
            continue

        root_elem = graph_model.find("root")
        if root_elem is None:
            _error(f"{prefix} Elemento <root> ausente dentro de <mxGraphModel>", errors)
            continue

        cells = root_elem.findall("mxCell")
        cell_ids: dict[str, ET.Element] = {}
        has_id0 = False
        has_id1 = False

        # --- Coleta todos os IDs e verifica as células-raiz ---
        for cell in cells:
            cid = cell.get("id")
            if cid is None:
                _error(f"{prefix} <mxCell> encontrado sem um atributo 'id'", errors)
                continue
            if cid in cell_ids:
                _error(f"{prefix} ID de célula duplicado id='{cid}'", errors)
            cell_ids[cid] = cell
            if cid == "0":
                has_id0 = True
            if cid == "1":
                has_id1 = True

        if not has_id0:
            _error(f"{prefix} Célula-raiz obrigatória id='0' ausente", errors)
        if not has_id1:
            _error(f"{prefix} Célula obrigatória da camada-padrão id='1' ausente", errors)

        # L2: id="0" deve ser a primeira célula; id="1", a segunda
        if len(cells) >= 1 and cells[0].get("id") != "0":
            _error(
                f"{prefix} A primeira <mxCell> deve ter id='0', "
                f"recebido id='{cells[0].get('id')}'",
                errors,
            )
        if len(cells) >= 2 and cells[1].get("id") != "1":
            _error(
                f"{prefix} A segunda <mxCell> deve ter id='1', "
                f"recebido id='{cells[1].get('id')}'",
                errors,
            )
        # L3: id="1" deve ter parent="0"
        for cell in cells:
            if cell.get("id") == "1" and cell.get("parent") != "0":
                _error(
                    f"{prefix} A célula id='1' deve ter parent='0', "
                    f"recebido parent='{cell.get('parent')}'",
                    errors,
                )
        # H2: cada página de diagrama deve conter uma célula de título
        # (um vértice cujo estilo contenha 'text;' e 'fontSize=18')
        def _is_title_style(style: str) -> bool:
            """Retorna True se a string de estilo identificar uma célula de título do draw.io."""
            return (
                (style.startswith("text;") or ";text;" in style)
                and "fontSize=18" in style
            )

        has_title_cell = any(
            c.get("vertex") == "1" and _is_title_style(c.get("style") or "")
            for c in cells
        )
        if not has_title_cell:
            _error(
                f"{prefix} Nenhuma célula de título encontrada; adicione um vértice com estilo "
                "que contenha 'text;' e 'fontSize=18' no topo da página",
                errors,
            )

        # --- Verifica a validade estrutural de cada célula ---
        for cell in cells:
            cid = cell.get("id", "<unknown>")
            is_vertex = cell.get("vertex") == "1"
            is_edge = cell.get("edge") == "1"

            # O pai deve existir (ignora a célula-raiz id=0, que não tem pai)
            parent = cell.get("parent")
            if cid != "0":
                if parent is None:
                    _error(f"{prefix} A célula id='{cid}' não tem o atributo 'parent'", errors)
                elif parent not in cell_ids:
                    _error(
                        f"{prefix} A célula id='{cid}' referencia parent='{parent}' desconhecido",
                        errors,
                    )

            # As células de vértice devem ter mxGeometry
            if is_vertex:
                geom = cell.find("mxGeometry")
                if geom is None:
                    _error(
                        f"{prefix} A célula de vértice id='{cid}' não tem <mxGeometry>",
                        errors,
                    )

            # As células de aresta devem ter source e target, e ambos devem existir.
            # Exceção: arestas flutuantes (por exemplo, linhas de vida de diagramas de sequência)
            # usam sourcePoint/targetPoint em mxGeometry em vez dos atributos source/target.
            if is_edge:
                source = cell.get("source")
                target = cell.get("target")
                geom = cell.find("mxGeometry")
                has_source_point = geom is not None and any(
                    p.get("as") == "sourcePoint" for p in geom.findall("mxPoint")
                )
                has_target_point = geom is not None and any(
                    p.get("as") == "targetPoint" for p in geom.findall("mxPoint")
                )
                if source is None and not has_source_point:
                    _error(
                        f"{prefix} A célula de aresta id='{cid}' não tem o atributo 'source' "
                        f"(nem sourcePoint em mxGeometry)",
                        errors,
                    )
                elif source is not None and source not in cell_ids:
                    _error(
                        f"{prefix} A aresta id='{cid}' referencia source='{source}' desconhecido",
                        errors,
                    )
                if target is None and not has_target_point:
                    _error(
                        f"{prefix} A célula de aresta id='{cid}' não tem o atributo 'target' "
                        f"(nem targetPoint em mxGeometry)",
                        errors,
                    )
                elif target is not None and target not in cell_ids:
                    _error(
                        f"{prefix} A aresta id='{cid}' referencia target='{target}' desconhecido",
                        errors,
                    )

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python validate-drawio.py <diagram.drawio>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Arquivo não encontrado: {path}")
        return 1
    if not path.is_file():
        print(f"Não é um arquivo: {path}")
        return 1

    print(f"Validando: {path}")
    errors = validate_file(path)

    if errors:
        print(f"\nFALHA: {len(errors)} erro(s) encontrado(s).")
        return 1

    print("APROVADO: nenhum erro encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
