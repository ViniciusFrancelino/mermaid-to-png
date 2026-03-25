from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


class MermaidRenderError(Exception):
    """Erro ao converter Mermaid para PNG."""
    pass


def mermaid_to_png(
    input_file: str | Path,
    output_file: str | Path | None = None,
    output_dir: str | Path | None = None,
    scale: int = 2,
    background_color: str = "white",
    timeout: int = 60,
) -> Path:
    """
    Converte um arquivo Mermaid (.mmd / .mermaid) em PNG usando o Mermaid CLI (mmdc).

    Args:
        input_file: Caminho do arquivo Mermaid de entrada.
        output_file: Caminho completo do PNG de saída. Se não for informado,
                     será gerado com o mesmo nome do arquivo de entrada.
        output_dir: Diretório onde o PNG será salvo, caso output_file não seja informado.
        scale: Escala da imagem. 1 = padrão. 2 costuma gerar melhor nitidez.
        background_color: Cor de fundo da imagem (ex.: "white", "transparent", "#ffffff").
        timeout: Tempo máximo da execução em segundos.

    Returns:
        Path do arquivo PNG gerado.

    Raises:
        FileNotFoundError: Se o arquivo de entrada não existir.
        ValueError: Se a extensão do arquivo de entrada for inválida.
        EnvironmentError: Se o Mermaid CLI não estiver instalado.
        MermaidRenderError: Se a renderização falhar.
    """
    input_path = Path(input_file).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    if input_path.suffix.lower() not in {".mmd", ".mermaid"}:
        raise ValueError(
            f"Extensão inválida para Mermaid: {input_path.suffix}. "
            "Use .mmd ou .mermaid."
        )

    if scale < 1:
        raise ValueError("O parâmetro 'scale' deve ser maior ou igual a 1.")

    mmdc_path = shutil.which("mmdc")
    if not mmdc_path:
        raise EnvironmentError(
            "Mermaid CLI (mmdc) não encontrado no PATH. "
            "Instale com: npm install -g @mermaid-js/mermaid-cli"
        )

    if output_file is not None:
        output_path = Path(output_file).expanduser().resolve()
        if output_path.suffix.lower() != ".png":
            output_path = output_path.with_suffix(".png")
    else:
        base_dir = Path(output_dir).expanduser().resolve() if output_dir else input_path.parent
        base_dir.mkdir(parents=True, exist_ok=True)
        output_path = base_dir / f"{input_path.stem}.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        mmdc_path,
        "-i", str(input_path),
        "-o", str(output_path),
        "-e", "png",
        "-s", str(scale),
        "-b", background_color,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise MermaidRenderError(
            f"Tempo limite excedido ao renderizar o arquivo: {input_path}"
        ) from exc
    except OSError as exc:
        raise MermaidRenderError(
            f"Falha ao executar o Mermaid CLI: {exc}"
        ) from exc

    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        details = stderr or stdout or "Sem detalhes retornados pelo Mermaid CLI."
        raise MermaidRenderError(
            "Falha ao converter Mermaid para PNG.\n"
            f"Arquivo: {input_path}\n"
            f"Comando: {' '.join(command)}\n"
            f"Detalhes: {details}"
        )

    if not output_path.exists():
        raise MermaidRenderError(
            "O comando foi executado, mas o arquivo PNG não foi encontrado na saída esperada.\n"
            f"Saída esperada: {output_path}"
        )

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte um arquivo Mermaid (.mmd/.mermaid) em PNG."
    )
    parser.add_argument("input_file", help="Arquivo Mermaid de entrada (.mmd ou .mermaid)")
    parser.add_argument(
        "-o", "--output-file",
        help="Caminho completo do PNG de saída. Ex.: ./saida/diagrama.png"
    )
    parser.add_argument(
        "-d", "--output-dir",
        help="Diretório de saída, caso --output-file não seja informado"
    )
    parser.add_argument(
        "-s", "--scale",
        type=int,
        default=2,
        help="Escala da imagem PNG (padrão: 2)"
    )
    parser.add_argument(
        "-b", "--background-color",
        default="white",
        help='Cor de fundo (padrão: "white"). Ex.: white, transparent, #ffffff'
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=60,
        help="Tempo máximo em segundos para renderização (padrão: 60)"
    )

    args = parser.parse_args()

    try:
        png_path = mermaid_to_png(
            input_file=args.input_file,
            output_file=args.output_file,
            output_dir=args.output_dir,
            scale=args.scale,
            background_color=args.background_color,
            timeout=args.timeout,
        )
        print(f"PNG gerado com sucesso: {png_path}")
    except Exception as exc:
        print(f"Erro: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
