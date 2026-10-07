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

def abrir_sistema_principal():
    global caixa_resultados, entry_nome, entry_preco, entry_quantidade, entry_baixa, janela

    # Destrói a janela de login antes de abrir a principal
    janela_login.destroy()

    # Tela principal do sistema
    janela = ctk.CTk()
    janela.title("Lanchonete Ennius Muniz - Senac-DF")
    janela.geometry("500x750")

    titulo = ctk.CTkLabel(janela, text="=== SISTEMA DE CONTROLE (SQLite) ===", font = ("Arial", 20, "bold"))
    titulo.pack(pady=20)

    entry_nome = ctk.CTkEntry(janela, placeholder_text="1. Nome do Produto", width = 350)
    entry_nome.pack(pady=10)

    entry_preco = ctk.CTkEntry(janela, placeholder_text="2. Preço (Ex: 5.00)", width=350)
    entry_preco.pack(pady=10)

    entry_quantidade = ctk.CTkEntry(janela, placeholder_text="3. Quantidade em estoque", width=350)
    entry_quantidade.pack(pady=10)

    btn_salvar = ctk.CTkButton(janela, text= "Salvar Produto", fg_color= "blue", command=cadastrar_produto)
    btn_salvar.pack(pady=15)

    btn_consultar = ctk.CTkButton(janela, text="Consultar Produtos", command=consultar_produtos, fg_color="orange")
    btn_consultar.pack(pady=10)

    # === Campo e Botão para dar Baixa no estoque
    entry_baixa = ctk.CTkEntry(janela, placeholder_text="Nome do Produto para Venda/Baixa", width=350)
    entry_baixa.pack(pady=8)

    btn_baixa = ctk.CTkButton(janela, text="Vender", command=dar_baixa_estoque, fg_color="green", hover_color="darkgreen")
    btn_baixa.pack(pady=8)

    caixa_resultados = ctk.CTkTextbox(janela, width=400, height=150)
    caixa_resultados.pack(pady=15)
    caixa_resultados.configure(state="disabled")


    # Configuração da etiqueta chamada "perigo" com a cor vermelha
    caixa_resultados.tag_config("perigo", foreground="red")
    caixa_resultados.configure(state="disabled")

    btn_encerrar = ctk.CTkButton(janela, text="Encerrar Sistema", command=encerrar_sistema, fg_color="red")
    btn_encerrar.pack(pady=10)

    janela.mainloop()

# === Funções de Lógica do Sistema ===
def consultar_produtos():
    conexao, cursor = conectar()
    cursor.execute("SELECT * FROM produtos")
    itens = cursor.fetchall()
    conexao.close()

    caixa_resultados.configure(state="normal")
    caixa_resultados.delete("1.0", "end")

    for linha in itens:
        nome_prod, preco_prod, qtd_prod = linha[0], linha[1], linha[2]
        texto = f"Produto: {linha[0]} | Preço: R$ {linha[1]:.2f} | Estoque: {linha[2]}\n"
        caixa_resultados.insert("end", texto)

        # Se a quantidade for menor que 5, insere aplicando a tag vermelha "perigo"abrir_sistema_principal
        if qtd_prod <= 5:
            caixa_resultados.insert("end", texto, "perigo")
        else:
            caixa_resultados.insert("end", texto)

    caixa_resultados.configure(state="disabled")

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

        if preco < 0 or quantidade < 0:
            messagebox.showwarning("Aviso", "Valores não podem ser negativos!")
            return # O 'return' expulsa o usuário da função antes de salvar

        conexao, cursor = conectar()

        # Checagem de Duplicidade: Procura no banco se o nome já existe
        cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))

            # Se o fetchone() encontrar algo, significa que já tem cadastro
        if cursor.fetchone():
            messagebox.showwarning("Aviso", "Este produto já está cadastrado!")
            entry_nome.delete(0,'end') # Limpa o campo para a nova tentativa
            return
            
        cursor.execute("INSERT INTO produtos VALUES (?, ?, ?)", (nome, preco, quantidade))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")

        entry_nome.delete(0, "end")
        entry_preco.delete(0, "end")
        entry_quantidade.delete(0, "end")
        
        consultar_produtos()

    except ValueError:
        messagebox.showerror("Erro de Digitação", "Digite valores numéricos válidos1")

def dar_baixa_estoque():
    nome_produto = entry_baixa.get().strip()
    if not nome_produto:
        messagebox.showwarning("Aviso", "Digite o nome do produto para dar baixa!")
        return

    conexao, cursor = conectar()
    cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome_produto,))
    resultado = cursor.fetchone()

    if resultado:
        qtd_atual = resultado[0]
        if qtd_atual > 0:
            nova_qtd = qtd_atual - 1
            cursor.execute("UPDATE produtos SET quantidade = ? WHERE nome = ?", (nova_qtd, nome_produto))
            conexao.commit()

            # Limpa o campo de texto da venda e atualiza a lista na tela na hora
            entry_baixa.delete(0,"end")
            consultar_produtos()

        else:   
            messagebox.showwarning("Esgotado", f"O produto '{nome_produto}' não possui saldo em estoque.")
    else:
        messagebox.showwarning("Erro", "Produto não encontrado!")

        conexao.close()

def encerrar_sistema():
    janela.destroy()

# Autenticação: ATUALIZAÇÃO 05/10
def validar_login():
    if entry_user.get() == "admin" and entry_senha.get() == "123":
        messagebox.showinfo("Autenticação", "Credenciais válidas!")
        abrir_sistema_principal() #Libera a inicialização do sistema

    else:
        messagebox.showerror("Erro de autenticação", "Credenciais inválidas.")
        entry_user.delete(0,"end")
        entry_senha.delete(0,"end")

# reogarnizei o código (06/10) atualizar lista de produtos
def atualizar_lista_produtos(nome_produto):
    conexao, cursor = conectar()
    cursor.execute("SELECT quantidade FROM produtos WHERE nome = ?", (nome_produto,))
    resultado = cursor.fetchone()

    if qtd_atual > 0: # Regra de negócio: Impede saldo negativo
        qtd_atual = resultado[0]

        nova_qtd  = qtd_atual -1 # Processamento da baixa na memória RAM
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE nome = ?", (nova_qtd, nome_produto))
        conexao.commit() # Confirmação da gravação no banco
        atualizar_lista_produtos()

    else: # Tratamento da exceção de saldo zero
        messagebox.showwarning("Aviso", "Produto Esgotado!")
    conexao.close()



# BLOCO A: INTERFACE DE LOGIN ATUALIZAÇÃO 05/10
janela_login = ctk.CTk()
janela_login.geometry("300x350")
janela_login.title("Tela de Login")

label_login = ctk.CTkLabel(janela_login, text= "Acesso ao Sistema", font=("Arial", 16, "bold"))
label_login.pack(pady=20)

entry_user = ctk.CTkEntry(janela_login, placeholder_text="Usuário")
entry_user.pack(pady=10)

# NOVO: Oculta o texto digitado na tela (senha) ATUALIZAÇÃO 05/10
entry_senha = ctk.CTkEntry(janela_login, placeholder_text="Senha", show="*")
entry_senha.pack(pady=10)

ctk.CTkButton(janela_login, text = "Autenticar", command=validar_login).pack(pady=30)

janela_login.mainloop()