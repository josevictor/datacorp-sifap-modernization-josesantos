#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador de planos do Terraform para atributos do tipo Set do AzureRM

Analisa a saída JSON do plano do Terraform para diferenciar:
- Alterações apenas de ordem (falsos positivos) em atributos do tipo Set
- Adições, exclusões e modificações reais

Uso:
    terraform show -json plan.tfplan | python analyze_plan.py
    python analyze_plan.py plan.json
    python analyze_plan.py plan.json --format json --exit-code

Para usar em pipelines de CI/CD, consulte o README.md deste diretório.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Códigos de saída da opção --exit-code
EXIT_NO_CHANGES = 0
EXIT_ORDER_ONLY = 0  # Alterações apenas de ordem não são alterações reais
EXIT_SET_CHANGES = 1  # Alterações reais em atributos Set
EXIT_RESOURCE_REPLACE = 2  # Substituição de recurso (mais grave)
EXIT_ERROR = 3

# Caminho padrão do arquivo JSON externo de atributos (relativo a este script)
DEFAULT_ATTRIBUTES_PATH = (
    Path(__file__).parent.parent / "references" / "azurerm_set_attributes.json"
)


# Configuração global
class Config:
    """Configuração global do analisador."""

    ignore_case: bool = False
    quiet: bool = False
    verbose: bool = False
    warnings: List[str] = []


CONFIG = Config()


def warn(message: str) -> None:
    """Adiciona uma mensagem de aviso."""
    CONFIG.warnings.append(message)
    if CONFIG.verbose:
        print(f"Aviso: {message}", file=sys.stderr)


def load_set_attributes(path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Carrega atributos do tipo Set de um arquivo JSON externo."""
    attributes_path = path or DEFAULT_ATTRIBUTES_PATH

    try:
        with open(attributes_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("resources", {})
    except FileNotFoundError:
        warn(f"Arquivo de atributos não encontrado: {attributes_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erro: JSON inválido no arquivo de atributos: {e}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


# Variável global que armazena os atributos carregados (inicializada em main)
AZURERM_SET_ATTRIBUTES: Dict[str, Any] = {}


def get_attr_config(attr_def: Any) -> tuple:
    """
    Analisa a definição do atributo e retorna (key_attr, nested_attrs).

    A definição do atributo pode ser:
    - str: atributo-chave simples (por exemplo, "name")
    - None/null: sem atributo-chave
    - dict: estrutura aninhada com "_key" e atributos aninhados
    """
    if attr_def is None:
        return (None, {})
    if isinstance(attr_def, str):
        return (attr_def, {})
    if isinstance(attr_def, dict):
        key_attr = attr_def.get("_key")
        nested_attrs = {k: v for k, v in attr_def.items() if k != "_key"}
        return (key_attr, nested_attrs)
    return (None, {})


@dataclass
class SetAttributeChange:
    """Representa uma alteração em um atributo do tipo Set."""

    attribute_name: str
    path: str = (
        ""  # Caminho completo dos atributos aninhados (por exemplo, "rewrite_rule_set.rewrite_rule")
    )
    order_only_count: int = 0
    added: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)
    modified: List[tuple] = field(default_factory=list)
    nested_changes: List["SetAttributeChange"] = field(default_factory=list)
    # Para sets primitivos (arrays de strings ou números)
    is_primitive: bool = False
    primitive_added: List[Any] = field(default_factory=list)
    primitive_removed: List[Any] = field(default_factory=list)


@dataclass
class ResourceChange:
    """Representa alterações em um único recurso."""

    address: str
    resource_type: str
    actions: List[str] = field(default_factory=list)
    set_changes: List[SetAttributeChange] = field(default_factory=list)
    other_changes: List[str] = field(default_factory=list)
    is_replace: bool = False
    is_create: bool = False
    is_delete: bool = False


@dataclass
class AnalysisResult:
    """Resultado geral da análise."""

    resources: List[ResourceChange] = field(default_factory=list)
    order_only_count: int = 0
    actual_set_changes_count: int = 0
    replace_count: int = 0
    create_count: int = 0
    delete_count: int = 0
    other_changes_count: int = 0
    warnings: List[str] = field(default_factory=list)


def get_element_key(element: Dict[str, Any], key_attr: Optional[str]) -> str:
    """Extrai o valor da chave de um elemento Set."""
    if key_attr and key_attr in element:
        val = element[key_attr]
        if CONFIG.ignore_case and isinstance(val, str):
            return val.lower()
        return str(val)
    # Usa como fallback o hash dos itens ordenados para elementos sem atributo-chave
    return str(hash(json.dumps(element, sort_keys=True)))


def normalize_value(val: Any) -> Any:
    """Normaliza valores para comparação (trata string vazia e None como equivalentes)."""
    if val == "" or val is None:
        return None
    if isinstance(val, list) and len(val) == 0:
        return None
    # Normaliza tipos numéricos (int versus float)
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val


def normalize_for_comparison(val: Any) -> Any:
    """Normaliza o valor para comparação, inclusive a opção sem diferenciação de caixa."""
    val = normalize_value(val)
    if CONFIG.ignore_case and isinstance(val, str):
        return val.lower()
    return val


def values_equivalent(before_val: Any, after_val: Any) -> bool:
    """Verifica se dois valores são efetivamente equivalentes."""
    return normalize_for_comparison(before_val) == normalize_for_comparison(after_val)


def compare_elements(
    before: Dict[str, Any], after: Dict[str, Any], nested_attrs: Dict[str, Any] = None
) -> tuple:
    """
    Compara dois elementos e retorna (simple_diffs, nested_set_attrs).

    simple_diffs: diferenças em atributos que não são Set
    nested_set_attrs: lista de (attr_name, before_val, after_val, attr_def) para Sets aninhados
    """
    nested_attrs = nested_attrs or {}
    simple_diffs = {}
    nested_set_attrs = []

    all_keys = set(before.keys()) | set(after.keys())

    for key in all_keys:
        before_val = before.get(key)
        after_val = after.get(key)

        # Verifica se este é um atributo Set aninhado
        if key in nested_attrs:
            if before_val != after_val:
                nested_set_attrs.append((key, before_val, after_val, nested_attrs[key]))
        elif not values_equivalent(before_val, after_val):
            simple_diffs[key] = {"before": before_val, "after": after_val}

    return (simple_diffs, nested_set_attrs)


def analyze_primitive_set(
    before_list: Optional[List[Any]],
    after_list: Optional[List[Any]],
    attr_name: str,
    path: str = "",
) -> SetAttributeChange:
    """Analisa alterações em um Set primitivo (array de strings ou números)."""
    full_path = f"{path}.{attr_name}" if path else attr_name
    change = SetAttributeChange(
        attribute_name=attr_name, path=full_path, is_primitive=True
    )

    before_set = set(before_list) if before_list else set()
    after_set = set(after_list) if after_list else set()

    # Aplica comparação sem diferenciar caixa, caso configurada
    if CONFIG.ignore_case:
        before_normalized = {v.lower() if isinstance(v, str) else v for v in before_set}
        after_normalized = {v.lower() if isinstance(v, str) else v for v in after_set}
    else:
        before_normalized = before_set
        after_normalized = after_set

    removed = before_normalized - after_normalized
    added = after_normalized - before_normalized

    if removed:
        change.primitive_removed = list(removed)
    if added:
        change.primitive_added = list(added)

    # Elementos presentes em ambos (apenas alteração de ordem)
    common = before_normalized & after_normalized
    if common and not removed and not added:
        change.order_only_count = len(common)

    return change


def analyze_set_attribute(
    before_list: Optional[List[Dict[str, Any]]],
    after_list: Optional[List[Dict[str, Any]]],
    key_attr: Optional[str],
    attr_name: str,
    nested_attrs: Dict[str, Any] = None,
    path: str = "",
    after_unknown: Optional[Dict[str, Any]] = None,
) -> SetAttributeChange:
    """Analisa alterações em um atributo do tipo Set, inclusive Sets aninhados."""
    full_path = f"{path}.{attr_name}" if path else attr_name
    change = SetAttributeChange(attribute_name=attr_name, path=full_path)
    nested_attrs = nested_attrs or {}

    before_list = before_list or []
    after_list = after_list or []

    # Trata valores que não são listas (elemento único)
    if not isinstance(before_list, list):
        before_list = [before_list] if before_list else []
    if not isinstance(after_list, list):
        after_list = [after_list] if after_list else []

    # Verifica se este é um set primitivo (elementos que não são dict)
    has_primitive_before = any(
        not isinstance(e, dict) for e in before_list if e is not None
    )
    has_primitive_after = any(
        not isinstance(e, dict) for e in after_list if e is not None
    )

    if has_primitive_before or has_primitive_after:
        # Trata sets primitivos
        return analyze_primitive_set(before_list, after_list, attr_name, path)

    # Cria mapas indexados pelo atributo-chave
    before_map: Dict[str, Dict[str, Any]] = {}
    after_map: Dict[str, Dict[str, Any]] = {}

    # Detecta chaves duplicadas
    for e in before_list:
        if isinstance(e, dict):
            key = get_element_key(e, key_attr)
            if key in before_map:
                warn(f"Chave duplicada '{key}' no estado anterior de {full_path}")
            before_map[key] = e

    for e in after_list:
        if isinstance(e, dict):
            key = get_element_key(e, key_attr)
            if key in after_map:
                warn(f"Chave duplicada '{key}' no estado posterior de {full_path}")
            after_map[key] = e

    before_keys = set(before_map.keys())
    after_keys = set(after_map.keys())

    # Localiza elementos removidos
    for key in before_keys - after_keys:
        display_key = key if key_attr else "(elemento)"
        change.removed.append(display_key)

    # Localiza elementos adicionados
    for key in after_keys - before_keys:
        display_key = key if key_attr else "(elemento)"
        change.added.append(display_key)

    # Compara elementos em comum
    for key in before_keys & after_keys:
        before_elem = before_map[key]
        after_elem = after_map[key]

        if before_elem == after_elem:
            # Correspondência exata: apenas alteração de ordem
            change.order_only_count += 1
        else:
            # Conteúdo alterado: verifica diferenças significativas
            simple_diffs, nested_set_list = compare_elements(
                before_elem, after_elem, nested_attrs
            )

            # Processa atributos Set aninhados recursivamente
            for nested_name, nested_before, nested_after, nested_def in nested_set_list:
                nested_key, sub_nested = get_attr_config(nested_def)
                nested_change = analyze_set_attribute(
                    nested_before,
                    nested_after,
                    nested_key,
                    nested_name,
                    sub_nested,
                    full_path,
                )
                if (
                    nested_change.order_only_count > 0
                    or nested_change.added
                    or nested_change.removed
                    or nested_change.modified
                    or nested_change.nested_changes
                    or nested_change.primitive_added
                    or nested_change.primitive_removed
                ):
                    change.nested_changes.append(nested_change)

            if simple_diffs:
                # Há diferenças reais em atributos não aninhados
                display_key = key if key_attr else "(elemento)"
                change.modified.append((display_key, simple_diffs))
            elif not nested_set_list:
                # Apenas diferenças entre null e vazio: trata como alteração de ordem
                change.order_only_count += 1

    return change


def analyze_resource_change(
    resource_change: Dict[str, Any],
    include_filter: Optional[List[str]] = None,
    exclude_filter: Optional[List[str]] = None,
) -> Optional[ResourceChange]:
    """Analisa a alteração de um único recurso do plano do Terraform."""
    resource_type = resource_change.get("type", "")
    address = resource_change.get("address", "")
    change = resource_change.get("change", {})
    actions = change.get("actions", [])

    # Ignora quando não há alteração ou não é um recurso AzureRM
    if actions == ["no-op"] or not resource_type.startswith("azurerm_"):
        return None

    # Aplica filtros
    if include_filter:
        if not any(f in resource_type for f in include_filter):
            return None
    if exclude_filter:
        if any(f in resource_type for f in exclude_filter):
            return None

    before = change.get("before") or {}
    after = change.get("after") or {}
    after_unknown = change.get("after_unknown") or {}
    before_sensitive = change.get("before_sensitive") or {}
    after_sensitive = change.get("after_sensitive") or {}

    # Determina o tipo de ação
    is_create = actions == ["create"]
    is_delete = actions == ["delete"]
    is_replace = "delete" in actions and "create" in actions

    result = ResourceChange(
        address=address,
        resource_type=resource_type,
        actions=actions,
        is_replace=is_replace,
        is_create=is_create,
        is_delete=is_delete,
    )

    # Ignora a análise detalhada de Set em criação/exclusão (todos os elementos são novos/removidos)
    if is_create or is_delete:
        return result

    # Obtém os atributos Set deste tipo de recurso
    set_attrs = AZURERM_SET_ATTRIBUTES.get(resource_type, {})

    # Analisa atributos do tipo Set
    analyzed_attrs: Set[str] = set()
    for attr_name, attr_def in set_attrs.items():
        before_val = before.get(attr_name)
        after_val = after.get(attr_name)

        # Avisa sobre atributos sensíveis
        if attr_name in before_sensitive or attr_name in after_sensitive:
            if before_sensitive.get(attr_name) or after_sensitive.get(attr_name):
                warn(
                    f"O atributo '{attr_name}' em {address} contém valores sensíveis (a comparação pode estar incompleta)"
                )

        # Ignora se o atributo não estiver presente ou não tiver sido alterado
        if before_val is None and after_val is None:
            continue
        if before_val == after_val:
            continue

        # Analisa apenas se for uma lista (Set no Terraform) ou tiver sido alterado
        if not isinstance(before_val, list) and not isinstance(after_val, list):
            continue

        # Analisa a definição do atributo para obter a chave e os atributos aninhados
        key_attr, nested_attrs = get_attr_config(attr_def)

        # Obtém after_unknown para este atributo
        attr_after_unknown = after_unknown.get(attr_name)

        set_change = analyze_set_attribute(
            before_val,
            after_val,
            key_attr,
            attr_name,
            nested_attrs,
            after_unknown=attr_after_unknown,
        )

        # Inclui apenas quando houver achados reais
        if (
            set_change.order_only_count > 0
            or set_change.added
            or set_change.removed
            or set_change.modified
            or set_change.nested_changes
            or set_change.primitive_added
            or set_change.primitive_removed
        ):
            result.set_changes.append(set_change)
            analyzed_attrs.add(attr_name)

    # Localiza outras alterações (que não sejam Set)
    all_keys = set(before.keys()) | set(after.keys())
    for key in all_keys:
        if key in analyzed_attrs:
            continue
        if key.startswith("_"):  # Ignora atributos internos
            continue
        before_val = before.get(key)
        after_val = after.get(key)
        if before_val != after_val:
            result.other_changes.append(key)

    return result


def collect_all_changes(set_change: SetAttributeChange, prefix: str = "") -> tuple:
    """
    Coleta recursivamente alterações apenas de ordem e alterações reais na estrutura aninhada.
    Retorna (order_only_list, actual_change_list)
    """
    order_only = []
    actual = []

    display_name = (
        f"{prefix}{set_change.attribute_name}" if prefix else set_change.attribute_name
    )

    has_actual_change = (
        set_change.added
        or set_change.removed
        or set_change.modified
        or set_change.primitive_added
        or set_change.primitive_removed
    )

    if set_change.order_only_count > 0 and not has_actual_change:
        order_only.append((display_name, set_change))
    elif has_actual_change:
        actual.append((display_name, set_change))

    # Processa alterações aninhadas
    for nested in set_change.nested_changes:
        nested_order, nested_actual = collect_all_changes(nested, f"{display_name}.")
        order_only.extend(nested_order)
        actual.extend(nested_actual)

    return (order_only, actual)


def format_set_change(change: SetAttributeChange, indent: int = 0) -> List[str]:
    """Formata um único SetAttributeChange para a saída."""
    lines = []
    prefix = "  " * indent

    # Trata sets primitivos
    if change.is_primitive:
        if change.primitive_added:
            lines.append(f"{prefix}**Adicionado:**")
            for item in change.primitive_added:
                lines.append(f"{prefix}  - {item}")
        if change.primitive_removed:
            lines.append(f"{prefix}**Removido:**")
            for item in change.primitive_removed:
                lines.append(f"{prefix}  - {item}")
        if change.order_only_count > 0:
            lines.append(f"{prefix}**Apenas ordem:** {change.order_only_count} elementos")
        return lines

    if change.added:
        lines.append(f"{prefix}**Adicionado:**")
        for item in change.added:
            lines.append(f"{prefix}  - {item}")

    if change.removed:
        lines.append(f"{prefix}**Removido:**")
        for item in change.removed:
            lines.append(f"{prefix}  - {item}")

    if change.modified:
        lines.append(f"{prefix}**Modificado:**")
        for item_key, diffs in change.modified:
            lines.append(f"{prefix}  - {item_key}:")
            for diff_key, diff_val in diffs.items():
                before_str = json.dumps(diff_val["before"], ensure_ascii=False)
                after_str = json.dumps(diff_val["after"], ensure_ascii=False)
                lines.append(f"{prefix}    - {diff_key}: {before_str} → {after_str}")

    if change.order_only_count > 0:
        lines.append(f"{prefix}**Apenas ordem:** {change.order_only_count} elementos")

    # Formata alterações aninhadas
    for nested in change.nested_changes:
        if (
            nested.added
            or nested.removed
            or nested.modified
            or nested.nested_changes
            or nested.primitive_added
            or nested.primitive_removed
        ):
            lines.append(f"{prefix}**Atributo aninhado `{nested.attribute_name}`:**")
            lines.extend(format_set_change(nested, indent + 1))

    return lines


def format_markdown_output(result: AnalysisResult) -> str:
    """Formata os resultados da análise como Markdown."""
    lines = ["# Resultados da análise do plano do Terraform", ""]
    lines.append(
        'Analisa alterações em atributos do tipo Set do AzureRM e identifica "diffs falsos positivos" apenas de ordem.'
    )
    lines.append("")

    # Categoriza as alterações (inclusive aninhadas)
    order_only_changes: List[tuple] = []
    actual_set_changes: List[tuple] = []
    replace_resources: List[ResourceChange] = []
    create_resources: List[ResourceChange] = []
    delete_resources: List[ResourceChange] = []
    other_changes: List[tuple] = []

    for res in result.resources:
        if res.is_replace:
            replace_resources.append(res)
        elif res.is_create:
            create_resources.append(res)
        elif res.is_delete:
            delete_resources.append(res)

        for set_change in res.set_changes:
            order_only, actual = collect_all_changes(set_change)
            for name, change in order_only:
                order_only_changes.append((res.address, name, change))
            for name, change in actual:
                actual_set_changes.append((res.address, name, change))

        if res.other_changes:
            other_changes.append((res.address, res.other_changes))

    # Seção: alterações apenas de ordem (falsos positivos)
    lines.append("## 🟢 Alterações apenas de ordem (sem impacto)")
    lines.append("")
    if order_only_changes:
        lines.append(
            "As alterações a seguir são apenas reordenações internas de atributos do tipo Set, sem alterações reais nos recursos."
        )
        lines.append("")
        for address, name, change in order_only_changes:
            lines.append(
                f"- `{address}`: **{name}** ({change.order_only_count} elements)"
            )
    else:
        lines.append("Nenhuma")
    lines.append("")

    # Seção: alterações reais em Set
    lines.append("## 🟡 Alterações reais em atributos Set")
    lines.append("")
    if actual_set_changes:
        for address, name, change in actual_set_changes:
            lines.append(f"### `{address}` - {name}")
            lines.append("")
            lines.extend(format_set_change(change))
            lines.append("")
    else:
        lines.append("Nenhuma")
    lines.append("")

    # Seção: substituições de recursos
    lines.append("## 🔴 Substituição de recurso (atenção)")
    lines.append("")
    if replace_resources:
        lines.append(
            "Os recursos a seguir serão excluídos e recriados. Isso pode causar indisponibilidade."
        )
        lines.append("")
        for res in replace_resources:
            lines.append(f"- `{res.address}`")
    else:
        lines.append("Nenhuma")
    lines.append("")

    # Seção: avisos
    if result.warnings:
        lines.append("## ⚠️ Avisos")
        lines.append("")
        for warning in result.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines)


def format_json_output(result: AnalysisResult) -> str:
    """Formata os resultados da análise como JSON."""

    def set_change_to_dict(change: SetAttributeChange) -> dict:
        d = {
            "attribute_name": change.attribute_name,
            "path": change.path,
            "order_only_count": change.order_only_count,
            "is_primitive": change.is_primitive,
        }
        if change.added:
            d["added"] = change.added
        if change.removed:
            d["removed"] = change.removed
        if change.modified:
            d["modified"] = [{"key": k, "diffs": v} for k, v in change.modified]
        if change.primitive_added:
            d["primitive_added"] = change.primitive_added
        if change.primitive_removed:
            d["primitive_removed"] = change.primitive_removed
        if change.nested_changes:
            d["nested_changes"] = [set_change_to_dict(n) for n in change.nested_changes]
        return d

    def resource_to_dict(res: ResourceChange) -> dict:
        return {
            "address": res.address,
            "resource_type": res.resource_type,
            "actions": res.actions,
            "is_replace": res.is_replace,
            "is_create": res.is_create,
            "is_delete": res.is_delete,
            "set_changes": [set_change_to_dict(c) for c in res.set_changes],
            "other_changes": res.other_changes,
        }

    output = {
        "summary": {
            "order_only_count": result.order_only_count,
            "actual_set_changes_count": result.actual_set_changes_count,
            "replace_count": result.replace_count,
            "create_count": result.create_count,
            "delete_count": result.delete_count,
            "other_changes_count": result.other_changes_count,
        },
        "has_real_changes": (
            result.actual_set_changes_count > 0
            or result.replace_count > 0
            or result.create_count > 0
            or result.delete_count > 0
            or result.other_changes_count > 0
        ),
        "resources": [resource_to_dict(r) for r in result.resources],
        "warnings": result.warnings,
    }
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_summary_output(result: AnalysisResult) -> str:
    """Formata os resultados da análise como um resumo de uma linha."""
    parts = []

    if result.order_only_count > 0:
        parts.append(f"🟢 {result.order_only_count} apenas de ordem")
    if result.actual_set_changes_count > 0:
        parts.append(f"🟡 {result.actual_set_changes_count} alterações de Set")
    if result.replace_count > 0:
        parts.append(f"🔴 {result.replace_count} substituições")

    if not parts:
        return "✅ Nenhuma alteração detectada"

    return " | ".join(parts)


def analyze_plan(
    plan_json: Dict[str, Any],
    include_filter: Optional[List[str]] = None,
    exclude_filter: Optional[List[str]] = None,
) -> AnalysisResult:
    """Analisa o JSON de um plano do Terraform e retorna os resultados."""
    result = AnalysisResult()

    resource_changes = plan_json.get("resource_changes", [])

    for rc in resource_changes:
        res = analyze_resource_change(rc, include_filter, exclude_filter)
        if res:
            result.resources.append(res)

            # Contabiliza estatísticas
            if res.is_replace:
                result.replace_count += 1
            elif res.is_create:
                result.create_count += 1
            elif res.is_delete:
                result.delete_count += 1

            if res.other_changes:
                result.other_changes_count += len(res.other_changes)

            for set_change in res.set_changes:
                order_only, actual = collect_all_changes(set_change)
                result.order_only_count += len(order_only)
                result.actual_set_changes_count += len(actual)

    # Adiciona avisos da configuração global
    result.warnings = CONFIG.warnings.copy()

    return result


def determine_exit_code(result: AnalysisResult) -> int:
    """Determina o código de saída com base nos resultados da análise."""
    if result.replace_count > 0:
        return EXIT_RESOURCE_REPLACE
    if (
        result.actual_set_changes_count > 0
        or result.create_count > 0
        or result.delete_count > 0
    ):
        return EXIT_SET_CHANGES
    return EXIT_NO_CHANGES


def parse_args() -> argparse.Namespace:
    """Analisa os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Analisa o JSON de um plano do Terraform para encontrar alterações em atributos do tipo Set do AzureRM.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Uso básico
  python analyze_plan.py plan.json

  # Por stdin
  terraform show -json plan.tfplan | python analyze_plan.py

  # CI/CD com código de saída
  python analyze_plan.py plan.json --exit-code

  # Saída JSON para processamento programático
  python analyze_plan.py plan.json --format json

  # Resumo para logs de CI
  python analyze_plan.py plan.json --format summary

Códigos de saída (com --exit-code):
  0 - Sem alterações ou apenas alterações de ordem
  1 - Alterações reais em atributos Set
  2 - Substituição de recurso detectada
  3 - Erro
""",
    )

    parser.add_argument(
        "plan_file",
        nargs="?",
        help="Caminho do arquivo JSON do plano do Terraform (lê de stdin se não for informado)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["markdown", "json", "summary"],
        default="markdown",
        help="Formato de saída (padrão: markdown)",
    )
    parser.add_argument(
        "--exit-code",
        "-e",
        action="store_true",
        help="Retorna o código de saída conforme a gravidade da alteração",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suprime avisos e a saída detalhada",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostra avisos detalhados e informações de depuração",
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Não diferencia maiúsculas de minúsculas ao comparar strings",
    )
    parser.add_argument(
        "--attributes", type=Path, help="Caminho do arquivo JSON personalizado de atributos"
    )
    parser.add_argument(
        "--include",
        action="append",
        help="Analisa apenas os recursos correspondentes a este padrão (pode ser repetido)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="Exclui os recursos correspondentes a este padrão (pode ser repetido)",
    )

    return parser.parse_args()


def main():
    """Ponto de entrada principal."""
    global AZURERM_SET_ATTRIBUTES

    args = parse_args()

    # Define as configurações globais
    CONFIG.ignore_case = args.ignore_case
    CONFIG.quiet = args.quiet
    CONFIG.verbose = args.verbose
    CONFIG.warnings = []

    # Carrega atributos Set do JSON externo
    AZURERM_SET_ATTRIBUTES = load_set_attributes(args.attributes)

    # Lê a entrada do plano
    if args.plan_file:
        try:
            with open(args.plan_file, "r") as f:
                plan_json = json.load(f)
        except FileNotFoundError:
            print(f"Erro: arquivo não encontrado: {args.plan_file}", file=sys.stderr)
            sys.exit(EXIT_ERROR)
        except json.JSONDecodeError as e:
            print(f"Erro: JSON inválido: {e}", file=sys.stderr)
            sys.exit(EXIT_ERROR)
    else:
        try:
            plan_json = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Erro: JSON inválido recebido de stdin: {e}", file=sys.stderr)
            sys.exit(EXIT_ERROR)

    # Verifica se o plano está vazio
    resource_changes = plan_json.get("resource_changes", [])
    if not resource_changes:
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "summary": {},
                        "has_real_changes": False,
                        "resources": [],
                        "warnings": [],
                    }
                )
            )
        elif args.format == "summary":
            print("✅ Nenhuma alteração detectada")
        else:
            print("# Resultados da análise do plano do Terraform\n")
            print("Nenhuma alteração de recurso detectada.")
        sys.exit(EXIT_NO_CHANGES)

    # Analisa o plano
    result = analyze_plan(plan_json, args.include, args.exclude)

    # Formata a saída
    if args.format == "json":
        output = format_json_output(result)
    elif args.format == "summary":
        output = format_summary_output(result)
    else:
        output = format_markdown_output(result)

    print(output)

    # Determina o código de saída
    if args.exit_code:
        sys.exit(determine_exit_code(result))


if __name__ == "__main__":
    main()
