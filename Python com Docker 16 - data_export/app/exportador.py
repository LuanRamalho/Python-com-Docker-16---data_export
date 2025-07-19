import csv
from database import obter_dados

def exportar_csv(nome_arquivo="exportacao.csv"):
    dados = obter_dados()
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["ID", "Disciplina", "Horas", "Data"])
        escritor.writerows(dados)
