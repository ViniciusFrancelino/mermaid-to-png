# 📊 Mermaid to PNG

Script em Python para converter arquivos **Mermaid (`.mmd`)** em imagens **PNG** de forma simples e rápida.

---

## 🚀 Funcionalidade

Este script:

1. Lê um arquivo `.mmd` (Mermaid)
2. Envia o conteúdo para a API pública `mermaid.ink`
3. Gera uma imagem PNG
4. Salva o arquivo no caminho especificado
5. Exibe o caminho absoluto do arquivo gerado

---

## 📦 Dependências

Instale as dependências com:

```bash
pip install requests

📁 Estrutura do Projeto
.
├── mermaid_to_png.py   # Script principal
├── diagrama.mmd        # Arquivo de entrada (Mermaid)
└── diagrama.png        # Saída gerada (PNG)
▶️ Como Executar
🔹 1. Entrada e saída personalizadas
python mermaid_to_png.py --input meu_arquivo.mmd --output resultado.png
🎨 2. Escolher tema do diagrama

Temas disponíveis:

default
dark
forest
neutral
python mermaid_to_png.py --input meu_arquivo.mmd --theme dark
⚙️ Parâmetros disponíveis
Parâmetro	Descrição
--input	Caminho do arquivo .mmd (padrão: diagrama.mmd)
--output	Nome do arquivo PNG de saída
--theme	Tema do diagrama
💡 Exemplo de uso
python mermaid_to_png.py --input fluxo.mmd --output fluxo.png --theme forest
🧠 Observações
É necessário conexão com a internet (usa API externa)
Ideal para automação, documentação e pipelines
Compatível com qualquer diagrama Mermaid