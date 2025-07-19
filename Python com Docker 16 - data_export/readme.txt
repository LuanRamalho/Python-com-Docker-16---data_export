# Sistema de Backup e Exportação - Python + Docker

## ✅ O que o sistema faz?

- Exporta todos os dados para um arquivo CSV
- Gera relatórios em PDF com gráficos de pizza e barras
- Interface gráfica moderna e colorida

---

## ▶️ Como executar o sistema

### 🔧 Pré-requisitos:
- Docker instalado
- Docker Compose instalado

---

### 🪟 Windows

1. Instale o X Server: Baixe e execute [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Execute o `XLaunch` com configurações padrão
3. No terminal, rode:

set DISPLAY=host.docker.internal:0.0
docker-compose up --build


---

### 🐧 Linux

1. Abra o terminal e digite:

xhost +
export DISPLAY=:0
docker-compose up --build


---

### 🍎 macOS

1. Instale o XQuartz: https://www.xquartz.org/
2. Reinicie o sistema após instalar
3. Execute:

xhost +
export DISPLAY=host.docker.internal:0
docker-compose up --build


---

### 📂 Arquivos gerados:

- `exportacao.csv` → Dados brutos exportados
- `relatorio.pdf` → Relatório visual com gráficos

---

## 👨‍💻 Desenvolvido em Python 3.10 com:
- `tkinter` (interface)
- `fpdf` (relatório PDF)
- `matplotlib` (gráficos)

