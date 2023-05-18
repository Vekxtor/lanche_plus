#Mensagens (prints) de carregamento deve ficar em VERDE
#Mensagens de falha em VERMELHO
#Nome de operadores em LARANJA

import sqlite3
conexao = sqlite3.connect('bank\BancoProdutos.sqlite3')
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
    comanda_off = int(input("DIGITE O NUMERO DA COMANDA: ")) # COMANDA DE MANIPULÇÃO DO OPERADOR
    # BUSCANDO NO BANCO DE DADOS SE A COMANDA ESTÁ DISPONÍVEL
    cursor.execute("SELECT id_comanda, nmr_comanda, nm_comanda, dt_aberto_comanda, usuario_id FROM Comanda")
    comanda_on = [] # COMANDA DE CONSULTA
    for comanda_on in cursor.fetchall():
        numero_da_comanda = comanda_on[0]
        operador = comanda_on[4]
        if comanda_off == comanda_on[1]: #A COMANDA JÁ ESTÁ ABERTA
            print("ESSA COMANDA JÁ ESTÁ EM UTILIZAÇÃO!")
            print(f'\033[33mCOMANDA: \033[37m{comanda_on[1]}\n\033[33mMESA: \033[37m{comanda_on[2]}\033[33m\nABERTO EM: \033[37m{comanda_on[3]}\033[33m')
            Operador(operador)
            Produtos(numero_da_comanda)

def Operador(operador): #BUSACNDO NA TABELA USUARIO QUEM FOI O GARÇOM QUE ABRIU A COMANDA
    cursor.execute(f'SELECT nm_usuario FROM Usuario WHERE id_usuario={operador};')
    garcom = []
    for garcom in cursor.fetchall():
        print(f'\033[33mABERTO POR: \033[37m{garcom[0]}')

def Produtos(comanda):
    print("\033[33mPRODUTOS CADASTRADOS NA COMANDA:\033[37m")
    for itens_da_comanda in cursor.execute(f'SELECT id_ProdutoComanda, produto_id, qtd_produto FROM ProdutoComanda WHERE id_ProdutoComanda={comanda};'):
        for produto_da_comanda in cursor.execute(f'SELECT nm_produto, vlr_produto FROM Produto WHERE id_produto = {itens_da_comanda[1]}'):
            total_produto = itens_da_comanda[2] * produto_da_comanda[1]
            print(f'\033[33m{itens_da_comanda[0]}) \033[37m{produto_da_comanda[0]} \033[33mx\033[37m {itens_da_comanda[2]} \033[33m=\033[37m {produto_da_comanda[1]}0 \033[33m|R$\033[37m {total_produto}0')
        

# SISTEMA DE ESCOLHA DE PRODUTOS
print('-'*50+'\n\033[33mBEM VINDO AO SISTEMA DE LANÇAMENTO DA LANCHE+\033[37m\n'+'-'*50)
Login()

conexao.commit()
conexao.close()