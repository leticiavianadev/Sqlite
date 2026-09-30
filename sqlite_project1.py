# Introdução ao sqlite - banco de dados - aula 23/09 (quarta-feira)
import sqlite3
import os

# Descobre exatamente onde este artquivo .py está salvo no computador
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, "sistema.db")

# Conecta ao banco usando o caminho completo e seguro
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

# --- FUNÇÕES DO SISTEMA ---

def cadastrar_produto():
    print("\n--- CADASTRO DE NOVOS PRODUTOS ---")
    while True:
        try:
            nome = input("1. Digite o nome do produto (ou digite 'sair' para voltar): ").strip()

            if nome.lower() == 'sair':
                break

            if not nome:
                print("O nome não pode estar vazio. Tente novamente.\n")
                continue

            preco = float(input("2. Digite o preco (R$) [Ex: 5.00]: "))
            quantidade = int(input("3. Digite a quantidade em estoque [Ex: 10]: "))

            cursor.execute("INSERT INTO produtos VALUES (?, ?, ?)", (nome, preco, quantidade))
            conexao.commit()

            print(f"-> Sucesso! Produto '{nome}' cadastrado.\n")

        except ValueError: # se for o valor errado, vai imprimir a mensagem
            print("Erro: Digite valores numéricos válidos para prelo e quantidade!\n")

def consultar_produto():
    print("\n --- CONSULTA DE PRODUTOS CADASTRADOS ---")

    cursor.execute("SELECT * FROM produtos")
    itens = cursor.fetchall()

    if not itens:
        print("Nenhum produto cadastrado no banco de dados até o momento.\n")
        return

    print("-" * 60)
    for linha in itens:
        print(f"Produto:")
        