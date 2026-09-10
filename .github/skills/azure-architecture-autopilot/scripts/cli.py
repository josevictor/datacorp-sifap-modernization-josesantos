#!/usr/bin/env python3
"""CLI do mecanismo de diagramas azure-architecture-autopilot."""
import argparse
import json
import sys
import os
import subprocess
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generator import generate_diagram


def main():
    parser = argparse.ArgumentParser(
        description="Gera diagramas interativos de arquitetura do Azure",
        prog="azure-architecture-autopilot"
    )
    parser.add_argument("-s", "--services", help="JSON de serviços (cadeia de texto ou caminho de arquivo)")
    parser.add_argument("-c", "--connections", help="JSON de conexões (cadeia de texto ou caminho de arquivo)")
    parser.add_argument("-t", "--title", default="Arquitetura do Azure", help="Título do diagrama")
    parser.add_argument("-o", "--output", default="azure-architecture.html", help="Caminho do arquivo de saída")
    parser.add_argument("-f", "--format", choices=["html", "png", "both"], default="html",
                        help="Formato de saída: html (padrão), png ou ambos (html+png)")
    parser.add_argument("--vnet-info", default="", help="Informações de CIDR da VNet")
    parser.add_argument("--hierarchy", default="", help="JSON da hierarquia de assinatura/RG")

    args = parser.parse_args()

    if not args.services or not args.connections:
        parser.error("-s/--services e -c/--connections são obrigatórios")

    services = _load_json(args.services, "services")
    connections = _load_json(args.connections, "connections")
    hierarchy = None
    if args.hierarchy:
        hierarchy = _load_json(args.hierarchy, "hierarchy")

    services = _normalize_services(services)
    connections = _normalize_connections(connections)

    html = generate_diagram(
        services=services,
        connections=connections,
        title=args.title,
        vnet_info=args.vnet_info,
        hierarchy=hierarchy,
    )

    # Determina os caminhos de saída
    out = Path(args.output)
    html_path = out.with_suffix(".html")
    png_path = out.with_suffix(".png")
    svg_path = out.with_suffix(".svg")

    if args.format in ("html", "both"):
        html_path.write_text(html, encoding="utf-8")
        print(f"HTML salvo: {html_path}")

    if args.format in ("png", "both"):
        # Grava o HTML temporário e captura a tela com puppeteer/playwright
        tmp_html = html_path if args.format == "both" else Path(str(png_path) + ".tmp.html")
        if args.format != "both":
            tmp_html.write_text(html, encoding="utf-8")

        success = _html_to_png(tmp_html, png_path)

        if args.format != "both" and tmp_html.exists():
            tmp_html.unlink()

        if success:
            print(f"PNG salvo: {png_path}")
        else:
            print("AVISO: Falha ao exportar o PNG. Instale o puppeteer (npm i puppeteer) para ter suporte a PNG.", file=sys.stderr)
            print(f"HTML salvo como alternativa: {html_path}")
            if not html_path.exists():
                html_path.write_text(html, encoding="utf-8")


def _html_to_png(html_path, png_path, width=1920, height=1080):
    """Converte HTML em PNG usando puppeteer (Node.js)."""
    node = shutil.which("node")
    if not node:
        return False

    # Tenta vários locais do puppeteer
    script = f"""
let puppeteer;
const paths = [
  'puppeteer',
  process.env.TEMP + '/node_modules/puppeteer',
  process.env.HOME + '/node_modules/puppeteer',
  './node_modules/puppeteer'
];
for (const p of paths) {{ try {{ puppeteer = require(p); break; }} catch(e) {{}} }}
if (!puppeteer) {{ console.error('puppeteer não encontrado'); process.exit(1); }}
(async () => {{
  const browser = await puppeteer.launch({{headless: 'new'}});
  const page = await browser.newPage();
  await page.setViewport({{width: {width}, height: {height}}});
  await page.goto('file:///{html_path.resolve().as_posix()}', {{waitUntil: 'networkidle0'}});
  await new Promise(r => setTimeout(r, 2000));
  await page.screenshot({{path: '{png_path.resolve().as_posix()}'}});
  await browser.close();
}})();
"""
    try:
        result = subprocess.run([node, "-e", script], capture_output=True, text=True, timeout=30)
        return result.returncode == 0 and png_path.exists()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _load_json(value, name):
    """Carrega JSON de uma string ou caminho de arquivo. Extrai a chave nomeada de um JSON combinado, se presente."""
    data = None
    if os.path.isfile(value):
        with open(value, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            data = json.loads(value)
        except json.JSONDecodeError as e:
            print(f"ERRO: JSON inválido para --{name}: {e}", file=sys.stderr)
            sys.exit(1)

    # Se os dados forem um dicionário com a chave nomeada, extrai-a (suporte a arquivo JSON combinado)
    if isinstance(data, dict) and name in data:
        return data[name]
    return data


def _normalize_services(services):
    """Normaliza os campos de serviço para maior tolerância."""
    for svc in services:
        if isinstance(svc.get("details"), str):
            svc["details"] = [svc["details"]]
        if isinstance(svc.get("private"), str):
            val = svc["private"].lower()
            if val in ("true", "1", "yes", "on"):
                svc["private"] = True
            elif val in ("false", "0", "no", "off"):
                svc["private"] = False
            else:
                # Registra um aviso para valores inválidos
                print(f"AVISO: Valor booleano inválido '{svc['private']}' para o campo 'private'. Usando False como padrão.", file=sys.stderr)
                svc["private"] = False
    return services


def _normalize_connections(connections):
    """Normaliza os campos de conexão para maior tolerância."""
    for conn in connections:
        if "type" not in conn:
            conn["type"] = "default"
    return connections


if __name__ == "__main__":
    main()
