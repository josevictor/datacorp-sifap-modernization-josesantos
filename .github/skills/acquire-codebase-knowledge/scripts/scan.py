#!/usr/bin/env python3
"""
scan.py: coleta informações de descoberta do projeto para a habilidade
acquire-codebase-knowledge.
Execute no diretório raiz do projeto.

Uso: python3 scan.py [OPÇÕES]

Opções:
  --output ARQUIVO   Grava a saída no ARQUIVO em vez de stdout
  --help             Exibe esta mensagem e encerra

Códigos de saída:
  0  Sucesso
  1  Erro de uso
"""

import os
import sys
import argparse
import subprocess
import json
from pathlib import Path
from typing import List, Set
import re

TREE_LIMIT = 200
TREE_MAX_DEPTH = 3
TODO_LIMIT = 60
MANIFEST_PREVIEW_LINES = 80
RECENT_COMMITS_LIMIT = 20
CHURN_LIMIT = 20

EXCLUDE_DIRS = {
    "node_modules", ".git", "dist", "build", "out", ".next", ".nuxt",
    "__pycache__", ".venv", "venv", ".tox", "target", "vendor",
    "coverage", ".nyc_output", "generated", ".cache", ".turbo",
    ".yarn", ".pnp", "bin", "obj"
}

MANIFESTS = [
    # JavaScript/Node.js
    "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "deno.json", "deno.jsonc",
    # Python
    "requirements.txt", "Pipfile", "Pipfile.lock", "pyproject.toml", "setup.py", "setup.cfg",
    "poetry.lock", "pdm.lock", "uv.lock",
    # Go
    "go.mod", "go.sum",
    # Rust
    "Cargo.toml", "Cargo.lock",
    # Java/Kotlin
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts",
    "gradle.properties",
    # PHP/Composer
    "composer.json", "composer.lock",
    # Ruby
    "Gemfile", "Gemfile.lock", "*.gemspec",
    # Elixir
    "mix.exs", "mix.lock",
    # Dart/Flutter
    "pubspec.yaml", "pubspec.lock",
    # .NET/C#
    "*.csproj", "*.sln", "*.slnx", "global.json", "packages.config",
    # Swift
    "Package.swift", "Package.resolved",
    # Scala
    "build.sbt", "scala-cli.yml",
    # Haskell
    "*.cabal", "stack.yaml", "cabal.project", "cabal.project.local",
    # OCaml
    "dune-project", "opam", "opam.lock",
    # Nim
    "*.nimble", "nim.cfg",
    # Crystal
    "shard.yml", "shard.lock",
    # R
    "DESCRIPTION", "renv.lock",
    # Julia
    "Project.toml", "Manifest.toml",
    # Sistemas de compilação
    "CMakeLists.txt", "Makefile", "GNUmakefile",
    "SConstruct", "build.xml",
    "BUILD", "BUILD.bazel", "WORKSPACE", "bazel.lock",
    "justfile", ".justfile", "Taskfile.yml",
    "tox.ini", "Vagrantfile"
]

ENTRY_CANDIDATES = [
    # JavaScript/Node.js/TypeScript
    "src/index.ts", "src/index.js", "src/index.mjs",
    "src/main.ts", "src/main.js", "src/main.py",
    "src/app.ts", "src/app.js",
    "src/server.ts", "src/server.js",
    "index.ts", "index.js", "app.ts", "app.js",
    "lib/index.ts", "lib/index.js",
    # Go
    "main.go", "cmd/main.go", "cmd/*/main.go",
    # Python
    "main.py", "app.py", "server.py", "run.py", "cli.py",
    "src/main.py", "src/__main__.py",
    # .NET/C#
    "Program.cs", "src/Program.cs", "Main.cs",
    # Java
    "Main.java", "Application.java", "App.java",
    "src/main/java/Main.java",
    # Kotlin
    "Main.kt", "Application.kt", "App.kt",
    # Rust
    "src/main.rs", "src/lib.rs",
    # Swift
    "main.swift", "Package.swift", "Sources/main.swift",
    # Ruby
    "app.rb", "main.rb", "lib/app.rb",
    # PHP
    "index.php", "app.php", "public/index.php",
    # Go
    "cmd/*/main.go",
    # Scala
    "src/main/scala/Main.scala",
    # Haskell
    "Main.hs", "app/Main.hs",
    # Clojure
    "src/core.clj", "-main.clj",
    # Elixir
    "lib/application.ex", "mix.exs",
]

LINT_FILES = [
    ".eslintrc", ".eslintrc.json", ".eslintrc.js", ".eslintrc.cjs", ".eslintrc.yml", ".eslintrc.yaml",
    "eslint.config.js", "eslint.config.mjs", "eslint.config.cjs",
    ".prettierrc", ".prettierrc.json", ".prettierrc.js", ".prettierrc.yml",
    "prettier.config.js", "prettier.config.mjs",
    ".editorconfig",
    "tsconfig.json", "tsconfig.base.json", "tsconfig.build.json",
    ".golangci.yml", ".golangci.yaml",
    "setup.cfg", ".flake8", ".pylintrc", "mypy.ini",
    ".rubocop.yml", "phpcs.xml", "phpstan.neon",
    "biome.json", "biome.jsonc"
]

ENV_TEMPLATES = [".env.example", ".env.template", ".env.sample", ".env.defaults", ".env.local.example"]

SOURCE_EXTS = [
    "ts", "tsx", "js", "jsx", "mjs", "cjs",
    "py", "go", "java", "kt", "rb", "php",
    "rs", "cs", "cpp", "c", "h", "ex", "exs",
    "swift", "scala", "clj", "cljs", "lua",
    "vim", "vim", "hs", "ml", "ml", "nim", "cr",
    "r", "jl", "groovy", "gradle", "xml", "json"
]

MONOREPO_FILES = ["pnpm-workspace.yaml", "lerna.json", "nx.json", "rush.json", "turbo.json", "moon.yml"]
MONOREPO_DIRS = ["packages", "apps", "libs", "services", "modules"]

CI_CD_CONFIGS = {
    ".github/workflows": "GitHub Actions",
    ".gitlab-ci.yml": "GitLab CI",
    "Jenkinsfile": "Jenkins",
    ".circleci/config.yml": "CircleCI",
    ".travis.yml": "Travis CI",
    "azure-pipelines.yml": "Azure Pipelines",
    "appveyor.yml": "AppVeyor",
    ".drone.yml": "Drone CI",
    ".woodpecker.yml": "Woodpecker CI",
    "bitbucket-pipelines.yml": "Bitbucket Pipelines"
}

CONTAINER_FILES = [
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".dockerignore", "Dockerfile.*",
    "k8s", "kustomization.yaml", "Chart.yaml",
    "Vagrantfile", "podman-compose.yml"
]

SECURITY_CONFIGS = [
    ".snyk", "security.txt", "SECURITY.md",
    ".dependabot.yml", ".whitesource",
    "sbom.json", "sbom.spdx", ".bandit.yaml"
]

PERFORMANCE_MARKERS = [
    "benchmark", "bench", "perf.data", ".prof",
    "k6.js", "locustfile.py", "jmeter.jmx"
]


def parse_args():
    """Analisa os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPÇÕES]",
        description="Varre o diretório atual (raiz do projeto) e gera informações de descoberta "
                    "para a habilidade acquire-codebase-knowledge.",
        add_help=False
    )
    parser._optionals.title = "opções"
    parser.add_argument(
        "--output",
        type=str,
        metavar="ARQUIVO",
        help="Grava a saída em ARQUIVO em vez de stdout"
    )
    parser.add_argument(
        "-h", "--help",
        action="help",
        help="Exibe esta mensagem e encerra"
    )
    return parser.parse_args()


def should_exclude(path: Path) -> bool:
    """Verifica se um caminho deve ser excluído da varredura."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def get_directory_tree(max_depth: int = TREE_MAX_DEPTH) -> List[str]:
    """Obtém a árvore de diretórios até max_depth."""
    files = []

    def walk(path: Path, depth: int):
        if depth > max_depth or should_exclude(path):
            return
        try:
            for item in sorted(path.iterdir()):
                if should_exclude(item):
                    continue
                rel_path = item.relative_to(Path.cwd())
                files.append(str(rel_path))
                if item.is_dir():
                    walk(item, depth + 1)
        except (PermissionError, OSError):
            pass

    walk(Path.cwd(), 0)
    return files[:TREE_LIMIT]


def find_manifest_files() -> List[str]:
    """Localiza arquivos de manifesto que correspondem aos padrões."""
    found = []
    for pattern in MANIFESTS:
        if "*" in pattern:
            # Trata padrões glob
            for path in Path.cwd().glob(pattern):
                if path.is_file() and not should_exclude(path):
                    found.append(path.name)
        else:
            path = Path.cwd() / pattern
            if path.is_file():
                found.append(pattern)
    return sorted(set(found))


def read_file_preview(filepath: Path, max_lines: int = MANIFEST_PREVIEW_LINES) -> str:
    """Lê o arquivo com um limite de linhas."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        if not lines:
            return "Nada encontrado."

        preview = ''.join(lines[:max_lines])
        if len(lines) > max_lines:
            preview += f"\n[TRUNCADO] Exibindo as primeiras {max_lines} de {len(lines)} linhas."
        return preview
    except Exception as e:
        return f"[Erro ao ler o arquivo: {e}]"


def find_entry_points() -> List[str]:
    """Localiza possíveis pontos de entrada."""
    found = []
    for candidate in ENTRY_CANDIDATES:
        if Path(candidate).exists():
            found.append(candidate)
    return found


def find_lint_config() -> List[str]:
    """Localiza arquivos de configuração de análise estática e formatação."""
    found = []
    for filename in LINT_FILES:
        if Path(filename).exists():
            found.append(filename)
    return found


def find_env_templates() -> List[tuple]:
    """Localiza modelos de variáveis de ambiente."""
    found = []
    for filename in ENV_TEMPLATES:
        path = Path(filename)
        if path.exists():
            found.append((filename, path))
    return found


def search_todos() -> List[str]:
    """Procura comentários TODO/FIXME/HACK."""
    todos = []
    patterns = ["TODO", "FIXME", "HACK"]
    exclude_dirs_str = "|".join(EXCLUDE_DIRS | {"test", "tests", "__tests__", "spec", "__mocks__", "fixtures"})

    try:
        for root, dirs, files in os.walk(Path.cwd()):
            # Remove diretórios excluídos de dirs para impedir que os.walk entre neles
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and d not in {"test", "tests", "__tests__", "spec", "__mocks__", "fixtures"}]

            for file in files:
                # Verifica a extensão do arquivo
                ext = Path(file).suffix.lstrip('.')
                if ext not in SOURCE_EXTS:
                    continue

                filepath = Path(root) / file
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        for line_num, line in enumerate(f, 1):
                            for pattern in patterns:
                                if pattern in line:
                                    rel_path = filepath.relative_to(Path.cwd())
                                    todos.append(f"{rel_path}:{line_num}: {line.strip()}")
                except Exception:
                    pass
    except Exception:
        pass

    return todos[:TODO_LIMIT]


def get_git_commits() -> List[str]:
    """Obtém os commits recentes do git."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", str(RECENT_COMMITS_LIMIT)],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        return []
    except Exception:
        return []


def get_git_churn() -> List[str]:
    """Obtém os arquivos com mais alterações nos últimos 90 dias."""
    try:
        result = subprocess.run(
            ["git", "log", "--since=90 days ago", "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        if result.returncode == 0:
            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            # Conta as ocorrências
            from collections import Counter
            counts = Counter(files)
            churn = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            return [f"{count:4d} {filename}" for filename, count in churn[:CHURN_LIMIT]]
        return []
    except Exception:
        return []


def is_git_repo() -> bool:
    """Verifica se o diretório atual é um repositório git."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            cwd=Path.cwd(),
            timeout=2
        )
        return True
    except Exception:
        return False


def detect_monorepo() -> List[str]:
    """Detecta sinais de monorepositório."""
    signals = []

    for filename in MONOREPO_FILES:
        if Path(filename).exists():
            signals.append(f"Ferramenta de monorepositório detectada: {filename}")

    for dirname in MONOREPO_DIRS:
        if Path(dirname).is_dir():
            signals.append(f"Diretório de subpacote encontrado: {dirname}/")

    # Verifica os workspaces de package.json
    if Path("package.json").exists():
        try:
            with open("package.json", 'r') as f:
                content = f.read()
                if '"workspaces"' in content:
                    signals.append("package.json tem o campo 'workspaces' (monorepositório com espaços de trabalho npm/yarn)")
        except Exception:
            pass

    return signals


def detect_ci_cd_pipelines() -> List[str]:
    """Detecta configurações de fluxos automatizados de CI/CD."""
    pipelines = []

    for config_path, pipeline_name in CI_CD_CONFIGS.items():
        path = Path(config_path)
        if path.is_file():
            pipelines.append(f"CI/CD: {pipeline_name}")
        elif path.is_dir():
            # Verifica arquivos de workflow no diretório
            try:
                if list(path.glob("*.yml")) or list(path.glob("*.yaml")):
                    pipelines.append(f"CI/CD: {pipeline_name}")
            except Exception:
                pass

    return pipelines


def detect_containers() -> List[str]:
    """Detecta configurações de conteinerização e orquestração."""
    containers = []

    for config in CONTAINER_FILES:
        path = Path(config)
        if path.is_file():
            if "Dockerfile" in config:
                containers.append("Contêiner: Docker encontrado")
            elif "docker-compose" in config:
                containers.append("Orquestração: Docker Compose encontrado")
            elif config.endswith(".yaml") or config.endswith(".yml"):
                containers.append(f"Contêiner/orquestração: {config}")
        elif path.is_dir():
            if config in ["k8s", "kubernetes"]:
                containers.append("Orquestração: configurações do Kubernetes encontradas")
            try:
                if list(path.glob("*.yml")) or list(path.glob("*.yaml")):
                    containers.append(f"Contêiner/orquestração: diretório {config}/ encontrado")
            except Exception:
                pass

    return containers


def detect_security_configs() -> List[str]:
    """Detecta configurações de segurança e conformidade."""
    security = []

    for config in SECURITY_CONFIGS:
        if Path(config).exists():
            config_name = config.replace(".yml", "").replace(".yaml", "").lstrip(".")
            security.append(f"Segurança: {config_name}")

    return security


def detect_performance_markers() -> List[str]:
    """Detecta marcadores de testes e análise de desempenho."""
    performance = []

    for marker in PERFORMANCE_MARKERS:
        if Path(marker).exists():
            performance.append(f"Desempenho: {marker} encontrado")
        else:
            # Verifica diretórios
            try:
                if Path(marker).is_dir():
                    performance.append(f"Desempenho: diretório {marker}/ encontrado")
            except Exception:
                pass

    return performance


def collect_code_metrics() -> dict:
    """Coleta métricas de código: arquivos por extensão e total de linhas."""
    metrics = {
        "total_files": 0,
        "by_extension": {},
        "by_language": {},
        "total_lines": 0,
        "largest_files": []
    }

    # Mapeamento de linguagens
    lang_map = {
        "ts": "TypeScript", "tsx": "TypeScript/React", "js": "JavaScript",
        "jsx": "JavaScript/React", "py": "Python", "go": "Go",
        "java": "Java", "kt": "Kotlin", "rs": "Rust",
        "cs": "C#", "rb": "Ruby", "php": "PHP",
        "swift": "Swift", "scala": "Scala", "ex": "Elixir",
        "cpp": "C++", "c": "C", "h": "Cabeçalho C",
        "clj": "Clojure", "lua": "Lua", "hs": "Haskell"
    }

    file_sizes = []

    try:
        for root, dirs, files in os.walk(Path.cwd()):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                filepath = Path(root) / file
                ext = filepath.suffix.lstrip('.')

                if not ext or ext in {"pyc", "o", "a", "so"}:
                    continue

                try:
                    size = filepath.stat().st_size
                    file_sizes.append((filepath.relative_to(Path.cwd()), size))

                    metrics["total_files"] += 1
                    metrics["by_extension"][ext] = metrics["by_extension"].get(ext, 0) + 1

                    lang = lang_map.get(ext, "Outros")
                    metrics["by_language"][lang] = metrics["by_language"].get(lang, 0) + 1

                    # Conta linhas de arquivos de texto
                    if ext in SOURCE_EXTS and size < 1_000_000:  # Ignora arquivos enormes
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                metrics["total_lines"] += len(f.readlines())
                        except Exception:
                            pass
                except Exception:
                    pass

        # Dez maiores arquivos
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        metrics["largest_files"] = [
            f"{str(f)}: {s/1024:.1f}KB" for f, s in file_sizes[:10]
        ]

    except Exception:
        pass

    return metrics


def print_section(title: str, content: List[str], output_file=None) -> None:
    """Imprime uma seção com título e conteúdo."""
    lines = [f"\n=== {title} ==="]

    if isinstance(content, list):
        lines.extend(content if content else ["Nada encontrado."])
    elif isinstance(content, str):
        lines.append(content)

    text = '\n'.join(lines) + '\n'

    if output_file:
        output_file.write(text)
    else:
        print(text, end='')


def main():
    """Ponto de entrada principal."""
    args = parse_args()

    output_file = None
    if args.output:
        output_dir = Path(args.output).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = open(args.output, 'w', encoding='utf-8')
        print(f"Gravando a saída em: {args.output}", file=sys.stderr)

    try:
        # Árvore de diretórios
        print_section(
            f"ÁRVORE DE DIRETÓRIOS (profundidade máxima {TREE_MAX_DEPTH}, somente arquivos-fonte)",
            get_directory_tree(),
            output_file
        )

        # Detecção do conjunto de tecnologias
        manifests = find_manifest_files()
        if manifests:
            manifest_content = [""]
            for manifest in manifests:
                manifest_path = Path(manifest)
                manifest_content.append(f"--- {manifest} ---")
                if manifest == "bun.lockb":
                    manifest_content.append("[Arquivo de bloqueio binário; consulte package.json para obter detalhes das dependências.]")
                else:
                    manifest_content.append(read_file_preview(manifest_path))
            print_section("DETECÇÃO DO CONJUNTO DE TECNOLOGIAS (arquivos de manifesto)", manifest_content, output_file)
        else:
            print_section("DETECÇÃO DO CONJUNTO DE TECNOLOGIAS (arquivos de manifesto)", ["Nenhum arquivo de manifesto reconhecido foi encontrado na raiz do projeto."], output_file)

        # Pontos de entrada
        entries = find_entry_points()
        if entries:
            entry_content = [f"Encontrado: {e}" for e in entries]
            print_section("PONTOS DE ENTRADA", entry_content, output_file)
        else:
            print_section("PONTOS DE ENTRADA", ["Nenhum ponto de entrada comum foi encontrado. Verifique 'main' ou 'scripts.start' nos arquivos de manifesto acima."], output_file)

        # Configuração de análise estática
        lint = find_lint_config()
        if lint:
            lint_content = [f"Encontrado: {l}" for l in lint]
            print_section("CONFIGURAÇÃO DE ANÁLISE ESTÁTICA E FORMATAÇÃO", lint_content, output_file)
        else:
            print_section("CONFIGURAÇÃO DE ANÁLISE ESTÁTICA E FORMATAÇÃO", ["Nenhum arquivo de configuração de análise estática ou formatação foi encontrado na raiz do projeto."], output_file)

        # Modelos de ambiente
        envs = find_env_templates()
        if envs:
            env_content = []
            for filename, filepath in envs:
                env_content.append(f"--- {filename} ---")
                env_content.append(read_file_preview(filepath))
            print_section("MODELOS DE VARIÁVEIS DE AMBIENTE", env_content, output_file)
        else:
            print_section("MODELOS DE VARIÁVEIS DE AMBIENTE", ["Nenhum .env.example ou .env.template foi encontrado. Identifique as variáveis de ambiente obrigatórias procurando leituras dessas variáveis no código e na configuração."], output_file)

        # TODOs
        todos = search_todos()
        if todos:
            print_section("TODO / FIXME / HACK (somente código de produção, diretórios de teste excluídos)", todos, output_file)
        else:
            print_section("TODO / FIXME / HACK (somente código de produção, diretórios de teste excluídos)", ["Nada encontrado."], output_file)

        # Informações do git
        if is_git_repo():
            commits = get_git_commits()
            if commits:
                print_section("COMMITS RECENTES DO GIT (últimos 20)", commits, output_file)
            else:
                print_section("COMMITS RECENTES DO GIT (últimos 20)", ["Nenhum commit encontrado."], output_file)

            churn = get_git_churn()
            if churn:
                print_section("ARQUIVOS COM MAIS ALTERAÇÕES (últimos 90 dias, 20 principais)", churn, output_file)
            else:
                print_section("ARQUIVOS COM MAIS ALTERAÇÕES (últimos 90 dias, 20 principais)", ["Nada encontrado."], output_file)
        else:
            print_section("COMMITS RECENTES DO GIT (últimos 20)", ["Não é um repositório git ou ainda não há commits."], output_file)
            print_section("ARQUIVOS COM MAIS ALTERAÇÕES (últimos 90 dias, 20 principais)", ["Não é um repositório git."], output_file)

        # Detecção de monorepositório
        monorepo = detect_monorepo()
        if monorepo:
            print_section("SINAIS DE MONOREPOSITÓRIO", monorepo, output_file)
        else:
            print_section("SINAIS DE MONOREPOSITÓRIO", ["Nenhum sinal de monorepositório foi detectado."], output_file)

        # Métricas de código
        metrics = collect_code_metrics()
        metrics_output = [
            f"Total de arquivos verificados: {metrics['total_files']}",
            f"Total de linhas de código: {metrics['total_lines']}",
            ""
        ]
        if metrics["by_language"]:
            metrics_output.append("Arquivos por linguagem:")
            for lang, count in sorted(metrics["by_language"].items(), key=lambda x: x[1], reverse=True):
                metrics_output.append(f"  {lang}: {count}")
        if metrics["largest_files"]:
            metrics_output.append("")
            metrics_output.append("Dez maiores arquivos:")
            metrics_output.extend(metrics["largest_files"])
        print_section("MÉTRICAS DE CÓDIGO", metrics_output, output_file)

        # Detecção de CI/CD
        ci_cd = detect_ci_cd_pipelines()
        if ci_cd:
            print_section("FLUXOS AUTOMATIZADOS DE CI/CD", ci_cd, output_file)
        else:
            print_section("FLUXOS AUTOMATIZADOS DE CI/CD", ["Nenhum fluxo automatizado de CI/CD foi detectado."], output_file)

        # Detecção de contêineres
        containers = detect_containers()
        if containers:
            print_section("CONTÊINERES E ORQUESTRAÇÃO", containers, output_file)
        else:
            print_section("CONTÊINERES E ORQUESTRAÇÃO", ["Nenhuma configuração de conteinerização foi detectada."], output_file)

        # Configurações de segurança
        security = detect_security_configs()
        if security:
            print_section("SEGURANÇA E CONFORMIDADE", security, output_file)
        else:
            print_section("SEGURANÇA E CONFORMIDADE", ["Nenhuma configuração de segurança foi detectada."], output_file)

        # Marcadores de desempenho
        performance = detect_performance_markers()
        if performance:
            print_section("DESEMPENHO E TESTES", performance, output_file)
        else:
            print_section("DESEMPENHO E TESTES", ["Nenhuma configuração de teste de desempenho foi detectada."], output_file)

        # Mensagem final
        final_msg = "\n=== VARREDURA CONCLUÍDA ===\n"
        if output_file:
            output_file.write(final_msg)
        else:
            print(final_msg, end='')

        return 0

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1

    finally:
        if output_file:
            output_file.close()


if __name__ == "__main__":
    sys.exit(main())
