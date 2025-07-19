from fpdf import FPDF
import matplotlib.pyplot as plt
from database import obter_dados
import os

def gerar_graficos():
    dados = obter_dados()
    disciplinas = {}
    for _, disciplina, horas, _ in dados:
        disciplinas[disciplina] = disciplinas.get(disciplina, 0) + horas

    # Gráfico de Pizza
    plt.figure(figsize=(5,5))
    plt.pie(disciplinas.values(), labels=disciplinas.keys(), autopct='%1.1f%%')
    plt.title("Distribuição de Horas por Disciplina")
    plt.savefig("grafico_pizza.png")

    # Gráfico de Barras
    plt.figure(figsize=(6,4))
    plt.bar(disciplinas.keys(), disciplinas.values(), color='skyblue')
    plt.title("Horas Totais por Disciplina")
    plt.ylabel("Horas")
    plt.savefig("grafico_barras.png")

def gerar_pdf(nome_arquivo="relatorio.pdf"):
    gerar_graficos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Relatório de Desempenho", ln=True, align="C")

    pdf.image("grafico_pizza.png", x=35, y=30, w=140)
    pdf.add_page()
    pdf.image("grafico_barras.png", x=30, y=30, w=150)

    pdf.output(nome_arquivo)
    os.remove("grafico_pizza.png")
    os.remove("grafico_barras.png")
