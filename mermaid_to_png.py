"""
mermaid_to_png.py
=================
Converte um arquivo .mmd (Mermaid) em uma imagem PNG.

Dependências:
    pip install requests

Estrutura dos arquivos:
    mermaid_to_png.py   ← script principal
    diagrama.mmd        ← seu arquivo Mermaid de entrada
    diagrama.png        ← imagem PNG gerada (saída)

Fluxo de execução:
    1. Lê o arquivo .mmd informado via argumento (ou padrão: diagrama.mmd)
    2. Envia o código para a API pública mermaid.ink
    3. Salva o PNG retornado no caminho de saída
    4. Exibe o caminho absoluto do arquivo gerado

Como executar:
    # Especificando entrada e saída
    python mermaid_to_png.py --input meu_arquivo.mmd --output resultado.png

    # Escolhendo tema (default | dark | forest | neutral)
    python mermaid_to_png.py --input meu_arquivo.mmd --theme dark
"""

import argparse
import base64
import sys
from pathlib import Path

import requests


# ---------------------------------------------------------------------------
# Exceção customizada
# ---------------------------------------------------------------------------

class MermaidConversionError(Exception):
    """Levantada quando a conversão do diagrama Mermaid falha."""


# ---------------------------------------------------------------------------
# Conversão
# ---------------------------------------------------------------------------

def mermaid_to_png(
    mermaid_code: str,
    output_path: str = "diagrama.png",
    timeout: int = 30,
    theme: str = "default",
) -> str:
    """
    Converte código Mermaid em uma imagem PNG via API mermaid.ink.

    Parâmetros
    ----------
    mermaid_code : str
        Conteúdo do diagrama Mermaid.
    output_path : str
        Caminho do arquivo PNG de saída.
    timeout : int
        Tempo limite da requisição HTTP em segundos.
    theme : str
        Tema visual: "default", "dark", "forest" ou "neutral".

    Retorna
    -------
    str
        Caminho absoluto do PNG gerado.

    Levanta
    -------
    ValueError
        Se o código Mermaid estiver vazio ou o tema for inválido.
    MermaidConversionError
        Se a requisição falhar ou o arquivo não puder ser salvo.
    """
    if not mermaid_code or not mermaid_code.strip():
        raise ValueError("O código Mermaid não pode ser vazio.")

    valid_themes = {"default", "dark", "forest", "neutral"}
    if theme not in valid_themes:
        raise ValueError(
            f"Tema inválido: '{theme}'. Escolha entre: {', '.join(sorted(valid_themes))}."
        )

    encoded = base64.urlsafe_b64encode(mermaid_code.encode("utf-8")).decode("ascii")
    api_url = f"https://mermaid.ink/img/{encoded}?theme={theme}"

    try:
        response = requests.get(api_url, timeout=timeout)
    except requests.exceptions.Timeout:
        raise MermaidConversionError(
            f"Timeout: a requisição excedeu {timeout} segundos."
        )
    except requests.exceptions.ConnectionError as exc:
        raise MermaidConversionError(
            f"Erro de conexão com a API do Mermaid Ink: {exc}"
        ) from exc

    if response.status_code != 200:
        raise MermaidConversionError(
            f"A API retornou status {response.status_code}. "
            "Verifique se o código Mermaid é válido."
        )

    if "image" not in response.headers.get("Content-Type", ""):
        raise MermaidConversionError(
            "A API não retornou uma imagem. Verifique a sintaxe do código Mermaid."
        )

    output_file = Path(output_path)
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_bytes(response.content)
    except OSError as exc:
        raise MermaidConversionError(
            f"Não foi possível salvar o arquivo '{output_path}': {exc}"
        ) from exc

    return str(output_file.resolve())


# ---------------------------------------------------------------------------
# Leitura do arquivo .mmd
# ---------------------------------------------------------------------------

def read_mmd_file(path: str) -> str:
    """Lê e retorna o conteúdo de um arquivo .mmd."""
    mmd_file = Path(path)

    if not mmd_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: '{path}'")

    if mmd_file.suffix.lower() not in {".mmd", ".md", ".txt"}:
        raise ValueError(
            f"Extensão não reconhecida: '{mmd_file.suffix}'. Use .mmd, .md ou .txt."
        )

    return mmd_file.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte um arquivo Mermaid (.mmd) em PNG.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        default="diagrama.mmd",
        help="Caminho do arquivo .mmd de entrada.",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Caminho do arquivo PNG de saída. Padrão: mesmo nome do input com extensão .png.",
    )
    parser.add_argument(
        "--theme", "-t",
        default="default",
        choices=["default", "dark", "forest", "neutral"],
        help="Tema visual do diagrama.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Tempo limite da requisição em segundos.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    output_path = args.output or str(Path(args.input).with_suffix(".png"))

    print(f"  Entrada : {args.input}")
    print(f"  Saída   : {output_path}")
    print(f"  Tema    : {args.theme}")
    print()

    try:
        mermaid_code = read_mmd_file(args.input)
        saved_path = mermaid_to_png(
            mermaid_code,
            output_path=output_path,
            theme=args.theme,
            timeout=args.timeout,
        )
        print(f"✔ PNG gerado com sucesso: {saved_path}")

    except FileNotFoundError as exc:
        print(f"✘ Arquivo não encontrado: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, MermaidConversionError) as exc:
        print(f"✘ Erro na conversão: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
