#Mensagens (prints) de carregamento deve ficar em VERDE
#Mensagens de falha em VERMELHO
#Nome de operadores em LARANJA

import sqlite3
conexao = sqlite3.connect('lanche_plus\BancoProdutos.sqlite3')
cursor = conexao.cursor()
#COMANDOS SQL EM FUNÇÕES
def Menu():
    cursor.execute("SELECT id_produto, nm_produto, vlr_produto FROM Produto;")
    produtos = []
    for produtos in cursor.fetchall():
        print(f"{produtos[0]}) {produtos[1]} - R${produtos[2]}")

def Escolha():
    escolha = int(input("Digite o número correspondete à sua escolha: "))
    produto_banco = cursor.execute("SELECT id_produto FROM Produto")
    
    for escolha in produto_banco.fetchall():
        if escolha == escolha:
            print(f'{escolha} = {produto_banco}')

def Login():
    cursor.execute("SELECT senha, nm_usuario FROM Usuario")
    usuario = int(input("DIGITE SUA SENHA: "))
    login = []
    print('\033[32mCARREGANDO INFORMAÇÕES...\033[37m')
    for login in cursor.fetchall():
        if usuario == login[0]:
            print(f'OPERADOR: \033[38;5;208m{login[1]}\033[37m')
            Comanda()

        else:
            print(f'USUÁRIO NÃO LOCALIZADO NO BANCO DE DADOS')
        break
    
def Comanda():
    return True

# SISTEMA DE ESCOLHA DE PRODUTOS
print('-'*50+'\n\033[33mBEM VINDO AO SISTEMA DE LANÇAMENTO DA LANCHE+\033[37m\n'+'-'*50)
Login()

conexao.commit()
conexao.close()