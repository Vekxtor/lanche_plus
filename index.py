import sqlite3
conexao = sqlite3.connect('BancoProdutos.sqlite3')
cursor = conexao.cursor()
#COMANDOS SQL EM FUNÇÕES
def Menu():
    cursor.execute("SELECT id_produto, nm_produto, vlr_produto FROM Produto;")
    produtos = []
    for produtos in cursor.fetchall():
        print(f"{produtos[0]}) {produtos[1]} - R${produtos[2]}")

def Escolha():
    escolha = int(input("Digite o número correspondete à sua escolha: "))    

# SISTEMA DE ESCOLHA DE PRODUTOS
while True:
    print('-'*30+'\n\033[33mESSE É O CARDÁPIO DA LANCHE+\033[37m\n'+'-'*30)
    Menu()


    conexao.commit()
    conexao.close()
    