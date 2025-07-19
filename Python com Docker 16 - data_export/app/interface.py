import tkinter as tk
from tkinter import messagebox
from exportador import exportar_csv
from relatorio import gerar_pdf
from database import criar_tabela, conectar, obter_dados

registro_selecionado = None  # global para identificar item selecionado

def salvar_ou_atualizar(disciplina, horas, data, atualizar_lista, limpar_campos):
    global registro_selecionado
    if not disciplina or not horas or not data:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return
    try:
        horas = int(horas)
    except ValueError:
        messagebox.showwarning("Erro", "Horas deve ser um número.")
        return

    with conectar() as conn:
        cursor = conn.cursor()
        if registro_selecionado:
            cursor.execute("""
                UPDATE desempenho
                SET disciplina = ?, horas = ?, data = ?
                WHERE id = ?
            """, (disciplina, horas, data, registro_selecionado))
            messagebox.showinfo("Atualizado", "Registro atualizado com sucesso.")
            registro_selecionado = None
        else:
            cursor.execute("INSERT INTO desempenho (disciplina, horas, data) VALUES (?, ?, ?)",
                           (disciplina, horas, data))
            messagebox.showinfo("Salvo", "Dados salvos com sucesso.")
        conn.commit()
    atualizar_lista()
    limpar_campos()

def excluir_registro(atualizar_lista, limpar_campos):
    global registro_selecionado
    if not registro_selecionado:
        messagebox.showwarning("Atenção", "Selecione um registro para excluir.")
        return
    resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir o registro?")
    if resposta:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM desempenho WHERE id = ?", (registro_selecionado,))
            conn.commit()
        messagebox.showinfo("Excluído", "Registro removido com sucesso.")
        registro_selecionado = None
        atualizar_lista()
        limpar_campos()

def executar_interface():
    global lista_ids
    lista_ids = []
    global registro_selecionado
    criar_tabela()

    janela = tk.Tk()
    janela.title("Backup e Exportação")
    janela.geometry("540x580")
    janela.configure(bg="#e0f7fa")

    tk.Label(janela, text="Backup e Exportação de Dados",
             font=("Arial", 16, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=10)

    # Entradas
    frame = tk.Frame(janela, bg="#e0f7fa")
    frame.pack()

    tk.Label(frame, text="Disciplina:", bg="#e0f7fa").grid(row=0, column=0, sticky="e")
    entrada_disciplina = tk.Entry(frame)
    entrada_disciplina.grid(row=0, column=1, padx=10)

    tk.Label(frame, text="Horas:", bg="#e0f7fa").grid(row=1, column=0, sticky="e")
    entrada_horas = tk.Entry(frame)
    entrada_horas.grid(row=1, column=1, padx=10)

    tk.Label(frame, text="Data (DD/MM/AAAA):", bg="#e0f7fa").grid(row=2, column=0, sticky="e")
    entrada_data = tk.Entry(frame)
    entrada_data.grid(row=2, column=1, padx=10)

    lista = tk.Listbox(janela, width=65, height=10)
    lista.pack(pady=10)

    def atualizar_lista():
        lista.delete(0, tk.END)
        dados = obter_dados()
        lista_ids.clear()
        for i, d in enumerate(dados, start=1):
            lista_ids.append(d[0])  # guardar ID real
            lista.insert(tk.END, f"{i} | {d[1]} | {d[2]}h | {d[3]}")


    def limpar_campos():
        entrada_disciplina.delete(0, tk.END)
        entrada_horas.delete(0, tk.END)
        entrada_data.delete(0, tk.END)

    def ao_selecionar(event):
        global registro_selecionado
        selecionado = lista.curselection()
        if selecionado:
            idx = selecionado[0]
            registro_selecionado = lista_ids[idx]  # ID real do banco
            item = lista.get(idx)
            partes = item.split(" | ")
            entrada_disciplina.delete(0, tk.END)
            entrada_disciplina.insert(0, partes[1])
            entrada_horas.delete(0, tk.END)
            entrada_horas.insert(0, partes[2].replace("h", ""))
            entrada_data.delete(0, tk.END)
            entrada_data.insert(0, partes[3])


    lista.bind("<<ListboxSelect>>", ao_selecionar)

    # Botões principais
    tk.Button(janela, text="Salvar / Atualizar", bg="#009688", fg="white",
              font=("Arial", 12), command=lambda: salvar_ou_atualizar(
                  entrada_disciplina.get(),
                  entrada_horas.get(),
                  entrada_data.get(),
                  atualizar_lista,
                  limpar_campos
              )).pack(pady=5)

    tk.Button(janela, text="Excluir", bg="#f44336", fg="white",
              font=("Arial", 12), command=lambda: excluir_registro(atualizar_lista, limpar_campos)).pack(pady=5)

    # Exportações
    tk.Button(janela, text="Exportar para CSV", bg="#4caf50", fg="white",
              font=("Arial", 12), command=lambda: [exportar_csv(), messagebox.showinfo("Sucesso", "Exportado para exportacao.csv")]).pack(pady=5)

    tk.Button(janela, text="Gerar Relatório PDF", bg="#2196f3", fg="white",
              font=("Arial", 12), command=lambda: [gerar_pdf(), messagebox.showinfo("Sucesso", "Relatório salvo como relatorio.pdf")]).pack(pady=5)

    atualizar_lista()
    janela.mainloop()
