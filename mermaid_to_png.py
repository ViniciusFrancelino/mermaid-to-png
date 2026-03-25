"""
mermaid_to_png.py
=================
Converte código Mermaid em imagem PNG.

Dependências:
    pip install requests

Estrutura dos arquivos:
    mermaid_to_png.py   ← script principal
    diagrama.mmd        ← arquivo Mermaid de entrada (modo arquivo)
    diagrama.png        ← imagem PNG gerada (saída)

Modos de uso
------------
1. Via arquivo .mmd (--mode file):
    python mermaid_to_png.py --mode file --input diagrama.mmd --output resultado.png

2. Via código inline no script (--mode inline):
    Edite a variável INLINE_CODE abaixo e execute:
    python mermaid_to_png.py --mode inline --output resultado.png

Argumentos disponíveis:
    --mode    file | inline       Fonte do código Mermaid (padrão: file)
    --input   caminho do .mmd     Obrigatório no modo file (padrão: diagrama.mmd)
    --output  caminho do .png     Padrão: diagrama.png
    --theme   default|dark|forest|neutral  (padrão: default)
    --timeout segundos            Padrão: 30
"""

import argparse
import base64
import sys
from pathlib import Path

import requests


# ---------------------------------------------------------------------------
# Código Mermaid inline — edite aqui para usar o modo inline
# ---------------------------------------------------------------------------

INLINE_CODE = """
flowchart TD
    A[Início] --> B[Tela de Login]

    B --> C[Inserir E-mail]
    C --> D[Inserir Senha]
    D --> E{Credenciais válidas?}

    E -- Não --> F[Exibir Erro]
    F --> G{Tentativas esgotadas?}
    G -- Não --> B
    G -- Sim --> H[Bloquear Conta]
    H --> I[Enviar E-mail de Desbloqueio]
    I --> FIM([Fim])

    E -- Sim --> J{Tem 2FA ativo?}
    J -- Não --> K[Redirecionar para Dashboard]
    J -- Sim --> L[Enviar Código por SMS ou E-mail]
    L --> M[Inserir Código 2FA]
    M --> N{Código válido?}
    N -- Não --> L
    N -- Sim --> K
    K --> FIM
"""


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
        description="Converte código Mermaid em PNG (via arquivo ou inline).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode", "-m",
        default="file",
        choices=["file", "inline"],
        help="Fonte do código Mermaid: 'file' lê um .mmd, 'inline' usa INLINE_CODE no script.",
    )
    parser.add_argument(
        "--input", "-i",
        default="diagrama.mmd",
        help="Caminho do arquivo .mmd (usado apenas no modo file).",
    )
    parser.add_argument(
        "--output", "-o",
        default="diagrama.png",
        help="Caminho do arquivo PNG de saída.",
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

    print(f"  Modo    : {args.mode}")
    if args.mode == "file":
        print(f"  Entrada : {args.input}")
    else:
        print(f"  Entrada : INLINE_CODE (definida no script)")
    print(f"  Saída   : {args.output}")
    print(f"  Tema    : {args.theme}")
    print()

    try:
        if args.mode == "file":
            mermaid_code = read_mmd_file(args.input)
        else:
            if not INLINE_CODE or not INLINE_CODE.strip():
                raise ValueError(
                    "A variável INLINE_CODE está vazia. "
                    "Edite-a no script antes de usar o modo inline."
                )
            mermaid_code = INLINE_CODE

        saved_path = mermaid_to_png(
            mermaid_code,
            output_path=args.output,
            theme=args.theme,
            timeout=args.timeout,
        )
        print(f"✔ PNG gerado com sucesso: {saved_path}")

    except FileNotFoundError as exc:
        print(f"✘ Arquivo não encontrado: {exc}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, MermaidConversionError) as exc:
        print(f"✘ Erro: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()