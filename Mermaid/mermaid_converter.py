import base64
import requests
import os
import argparse

def converter_mermaid_para_png(codigo_mermaid: str, caminho_saida: str) -> bool:
    """
    Converte uma string contendo código Mermaid em uma imagem PNG usando a API mermaid.ink.
    """
    try:
        mermaid_bytes = codigo_mermaid.encode('utf-8')
        base64_bytes = base64.b64encode(mermaid_bytes)
        base64_string = base64_bytes.decode('utf-8')

        url = f"https://mermaid.ink/img/{base64_string}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(caminho_saida, 'wb') as arquivo_imagem:
            arquivo_imagem.write(response.content)

        print(f"Sucesso: Imagem salva como '{caminho_saida}'")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"Erro na API (Possível sintaxe inválida no Mermaid). Status: {e.response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: Não foi possível acessar a API do Mermaid. Detalhes: {e}")
        return False
    except IOError as e:
        print(f"Erro de sistema de arquivos: Não foi possível salvar a imagem. Detalhes: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False

def converter_arquivo_para_png(caminho_arquivo_entrada: str, caminho_saida: str) -> bool:
    """
    Lê o código Mermaid de um arquivo de texto e repassa para a função de conversão.
    """
    try:
        with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            codigo_lido = arquivo.read()
            
        return converter_mermaid_para_png(codigo_lido, caminho_saida)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo_entrada}' não foi encontrado na pasta atual.")
        return False
    except Exception as e:
        print(f"Erro inesperado ao tentar ler o arquivo: {e}")
        return False

# ---------------------------------------------------------
# Configuração para rodar via Terminal (Linha de Comando)
# ---------------------------------------------------------
if __name__ == "__main__":
    # Cria o interpretador de comandos do terminal
    parser = argparse.ArgumentParser(description="Converte arquivos de texto com código Mermaid para imagens PNG.")
    
    # Define que o programa exige receber o nome de um arquivo
    parser.add_argument("arquivo_entrada", help="O nome do arquivo .txt ou .mmd contendo o código (ex: diagrama.txt)")
    
    # Lê o que você digitou no terminal
    args = parser.parse_args()
    
    arquivo_origem = args.arquivo_entrada
    
    # Gera o nome do arquivo de saída automaticamente (troca a extensão para .png)
    # Exemplo: de "meu_projeto.txt" para "meu_projeto.png"
    nome_sem_extensao, _ = os.path.splitext(arquivo_origem)
    arquivo_destino = f"{nome_sem_extensao}.png"
    
    print(f"Lendo o arquivo '{arquivo_origem}'...")
    
    # Executa a conversão
    sucesso = converter_arquivo_para_png(arquivo_origem, arquivo_destino)
    
    if not sucesso:
        print("A conversão falhou.")