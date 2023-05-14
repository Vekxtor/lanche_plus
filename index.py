import sqlite3
conexao = sqlite3.connect('lanche_plus\BancoProdutos.sqlite3')
cursor = conexao.cursor()
#COMANDOS SQL
def Menu():
    cursor.execute("SELECT id_produto, nm_produto, vlr_produto FROM Produto;")
    produtos = []
    for produtos in cursor.fetchall():
        print(f"{produtos[0]} - {produtos[1]} - {produtos[2]}")


# SISTEMA DE ESCOLHA DE PRODUTOS
Menu()

conexao.commit()
conexao.close()