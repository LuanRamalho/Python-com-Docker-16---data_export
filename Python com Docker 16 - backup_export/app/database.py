import sqlite3

def conectar():
    return sqlite3.connect("dados.db")

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS desempenho (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina TEXT,
                horas INTEGER,
                data TEXT
            )
        """)
        conn.commit()

def obter_dados():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM desempenho")
        return cursor.fetchall()
