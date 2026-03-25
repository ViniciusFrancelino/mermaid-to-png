# 📊 Mermaid to PNG

Script Python para converter diagramas **Mermaid** em imagens **PNG**, com suporte a duas formas de entrada: **arquivo `.mmd`** ou **código inline no script**.

---

## 🚀 Funcionalidades

- Converte qualquer diagrama Mermaid em PNG
- Dois modos de entrada: **arquivo** ou **inline**
- Suporte a 4 temas visuais
- Tratamento de erros claro e objetivo
- Sem dependências pesadas — apenas `requests`

---

## 📦 Dependência

```bash
pip install requests
```

> Requer **Python 3.10+** e **conexão com a internet** (usa a API pública `mermaid.ink`).

---

## 📁 Estrutura do Projeto

```
.
├── mermaid_to_png.py   # Script principal
├── diagrama.mmd        # Arquivo de entrada (modo file)
└── diagrama.png        # Imagem PNG gerada (saída)
```

---

## ▶️ Como Executar

O script possui dois modos de uso, controlados pelo argumento `--mode`.

---

### 📄 Modo `file` — lê um arquivo `.mmd` (padrão)

```bash
# Usando os valores padrão (diagrama.mmd → diagrama.png)
python mermaid_to_png.py

# Especificando entrada e saída
python mermaid_to_png.py --mode file --input meu_arquivo.mmd --output resultado.png
```

---

### ✏️ Modo `inline` — código escrito direto no script

Edite a variável `INLINE_CODE` no topo do arquivo `mermaid_to_png.py`:

```python
INLINE_CODE = """
graph TD
    A[Início] --> B[Processo]
    B --> C[Fim]
"""
```

Depois execute:

```bash
python mermaid_to_png.py --mode inline --output resultado.png
```

---

## ⚙️ Parâmetros Disponíveis

| Parâmetro  | Opções                              | Padrão        | Descrição                                      |
|------------|-------------------------------------|---------------|------------------------------------------------|
| `--mode`   | `file`, `inline`                    | `file`        | Fonte do código Mermaid                        |
| `--input`  | caminho do arquivo                  | `diagrama.mmd`| Arquivo `.mmd` de entrada (somente modo file)  |
| `--output` | caminho do arquivo                  | `diagrama.png`| Arquivo PNG de saída                           |
| `--theme`  | `default`, `dark`, `forest`, `neutral` | `default`  | Tema visual do diagrama                        |
| `--timeout`| número inteiro                      | `30`          | Tempo limite da requisição em segundos         |

---

## 💡 Exemplos

```bash
# Modo file com tema escuro
python mermaid_to_png.py --mode file --input fluxo.mmd --output fluxo.png --theme dark

# Modo inline com tema forest
python mermaid_to_png.py --mode inline --output diagrama.png --theme forest

# Modo file com timeout maior
python mermaid_to_png.py --mode file --input diagrama.mmd --timeout 60
```

---

## 🧠 Observações

- No modo `file`, o arquivo deve ter extensão `.mmd`, `.md` ou `.txt`
- No modo `inline`, a variável `INLINE_CODE` não pode estar vazia
- O PNG é salvo no caminho exato informado em `--output`
- Erros de sintaxe no Mermaid são reportados com mensagem clara no terminal
