# Introdução ao sqlite - banco de dados - aula 23/09 (quarta-feira)
import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def conectar():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "sistema.db")

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

# Cria a tabela caso ela ainda não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            nome TEXT,
            preco REAL,
            quantidade INTEGER
        )
    """)
    conexao.commit() #como se fosse o botão salvar, ele guarda a informação, logo abaixo há um loop.
    return conexao, cursor

def cadastrar_produto():
    nome = entry_nome.get().strip()
    preco_str = entry_preco.get().strip()
    quantidade_str = entry_quantidade.get().strip()

    if not nome:
        messagebox.showwarning("Aviso", "O nome do produto não pode ficar vazio")
        return

    try:
        preco = float(preco_str)
        quantidade = int(quantidade_str)

        conexao, cursor = conectar()
        cursor.execute("INSERT INTO produtos VALUES (?, ?, ?)", (nome, preco, quantidade))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_quantidade.delete(0, "end")
        
        consultar_produto()

    except ValueError:
        messagebox.showerror("Erro de Digitação", "Digite valores numéricos válidos1")

def consultar_produto():
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM produtos")
    itens = cursor.fetchall()
    conexao.close()

    caixa_resultados.configure(state="normal")
    caixa_resultados.delete("1.0", "end")

    for linha in itens:
        texto = f"Produto: {linha[0]:15} | Preço: R$ {linha[1]:6.2f} | Estoque: {linha[2]}\n"
        caixa_resultados.insert("end", texto)

    caixa_resultados.configure(state="disabled")

def encerrar_sistema():
    messagebox.showinfo("Aviso!", "Sistema encerrando...")
    janela.destroy()


janela = ctk.CTk()
janela.title("Lanchonete Ennius Muniz - Senac-DF")
janela.geometry("650x650")

titulo = ctk.CTkLabel(janela, text="=== SISTEMA DE CONTROLE (SQLite) ===", font = ("Arial", 16, "bold"))
titulo.pack(pady=20)

entry_nome = ctk.CTkEntry(janela, placeholder_text="1. Nome do Produto", width = 350)
entry_nome.pack(pady=10)

entry_preco = ctk.CTkEntry(janela, placeholder_text="2. Preço (Ex: 5.00)", width=350)
entry_preco.pack(pady=10)

entry_quantidade = ctk.CTkEntry(janela, placeholder_text="3. Quantidade em estoque", width=350)
entry_quantidade.pack(pady=10)

btn_salvar = ctk.CTkButton(janela, text= "Salvar Produto", fg_color= "green", command=cadastrar_produto)
btn_salvar.pack(pady=15)

btn_consultar = ctk.CTkButton(janela, text="Consultar Produtos Salvos", command=consultar_produto)
btn_consultar.pack(pady=10)

btn_encerrar = ctk.CTkButton(janela, text="Encerrar Sistema", command=encerrar_sistema, fg_color="red")
btn_encerrar.pack(pady=5)

caixa_resultados = ctk.CTkTextbox(janela, width=450, height=200, font=("Courier", 12))
caixa_resultados.pack(pady=20)
caixa_resultados.configure(state="disabled")

janela.mainloop()
