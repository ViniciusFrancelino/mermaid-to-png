# 🧜‍♂️ Conversor de Mermaid para PNG (CLI)

Um utilitário de linha de comando (CLI) desenvolvido em Python para converter diagramas de texto no formato [Mermaid](https://mermaid.js.org/) (`.txt` ou `.mmd`) em imagens de alta qualidade (`.png`).

Este projeto foi desenhado para ser leve e rápido. Em vez de exigir a instalação local de pacotes pesados como o Node.js ou o `@mermaid-js/mermaid-cli`, ele processa a conversão codificando o diagrama em Base64 e consumindo a API pública do [mermaid.ink](https://mermaid.ink/).

---

## 📑 Índice

1. [Como Funciona](#-como-funciona)
2. [Pré-requisitos](#-pré-requisitos)
3. [Instalação e Configuração](#-instalação-e-configuração)
4. [Como Usar](#-como-usar)
5. [Exemplos Práticos](#-exemplos-práticos)
6. [Tratamento de Erros](#-tratamento-de-erros)
7. [Estrutura do Código](#-estrutura-do-código)

---

## ⚙️ Como Funciona

O fluxo de execução do script segue três etapas principais:
1. **Leitura:** O script recebe o caminho de um arquivo de texto local via terminal e lê o código Mermaid contido nele.
2. **Codificação:** O texto extraído é convertido em bytes UTF-8 e, em seguida, codificado no formato Base64.
3. **Requisição e Download:** Uma URL é montada apontando para a API `https://mermaid.ink/img/{base64}`. O script faz uma requisição HTTP GET e salva a resposta (os bytes da imagem) em um arquivo `.png` com o mesmo nome do arquivo original.

---

## 🛠️ Pré-requisitos

Para executar este projeto, sua máquina precisa atender aos seguintes requisitos:

* **Python 3.6** ou superior instalado e adicionado ao `PATH` do sistema.
* Acesso à internet (necessário para a comunicação com a API).

---

## 📦 Instalação e Configuração

Nenhuma configuração complexa é necessária. Siga os passos abaixo:

1. Salve o script Python na sua pasta de trabalho (ex: `mermaid_converter.py`).
2. Abra o terminal na pasta do projeto.
3. Instale a biblioteca `requests`, que é a única dependência externa utilizada para fazer as chamadas HTTP:

```bash
pip install requests