#Mensagens (prints) de carregamento deve ficar em VERDE
#Mensagens de falha em VERMELHO
#Nome de operadores em LARANJA
import pandas as pd
import sqlite3
from datetime import datetime
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
    usuario = int(input("DIGITE SUA SENHA: "))
    cursor.execute("SELECT senha, nm_usuario, id_usuario FROM Usuario WHERE senha = ?", (usuario,))
    print('\033[32mCARREGANDO INFORMAÇÕES...\033[37m')

    login = cursor.fetchone()  # Recupera apenas um resultado

    if login is not None and usuario == login[0]:
        id_usuario = login[2]
        print(f'OPERADOR: \033[38;5;208m{login[1]}\033[37m')
        Comanda(id_usuario)
    else:
        print('\033[91mSENHA INVÁLIDA\033[0m')


    
def Comanda(id_usuario):
    comanda_off = int(input("DIGITE O NUMERO DA COMANDA: ")) #COMANDA DE MANIPULÇÃO DO OPERADOR
    #BUSCANDO NO BANCO DE DADOS SE A COMANDA ESTÁ DISPONÍVEL
    cursor.execute("SELECT id_comanda, nmr_comanda, nm_comanda, dt_aberto_comanda, usuario_id FROM Comanda WHERE nmr_comanda = ?", (comanda_off,))
    comanda_on = cursor.fetchone()
    
    if comanda_on is not None and comanda_off == comanda_on[1]:
        numero_da_comanda = comanda_on[0]
        operador = comanda_on[4]
        
        print("ESSA COMANDA JÁ ESTÁ EM UTILIZAÇÃO!")
        print(f'\033[33mCOMANDA: \033[37m{comanda_on[1]}\n\033[33mMESA: \033[37m{comanda_on[2]}\033[33m\nABERTO EM: \033[37m{comanda_on[3]}\033[33m')
        Operador(operador)
        Produtos(numero_da_comanda)

    else:
        print('\033[91m' + 'ESTA COMANDA ESTÁ VAZIA' + '\033[0m')
        CriarComanda(comanda_off, id_usuario)

def CriarComanda(comanda, id_usuario):
    NmrMesa = int(input('DIGITE O NÚMERO DA MESA: '))
    agora = datetime.now()
    horario_atual = agora.strftime("%H:%M:%S")
    cursor.execute("INSERT INTO Comanda (nmr_comanda, nm_comanda, dt_aberto_comanda, usuario_id) VALUES (?, ?, ?, ?)", (comanda, NmrMesa, horario_atual, id_usuario,))
    conexao.commit()
    Lancamento()

def Lancamento():
    return True

def Operador(operador): #BUSACNDO NA TABELA USUARIO QUEM FOI O GARÇOM QUE ABRIU A COMANDA
    cursor.execute(f'SELECT nm_usuario FROM Usuario WHERE id_usuario={operador};')
    garcom = []
    for garcom in cursor.fetchall():
        print(f'\033[33mABERTO POR: \033[37m{garcom[0]}')

def Produtos(comanda):
    print("\033[33mPRODUTOS CADASTRADOS NA COMANDA:\033[37m")
    comanda_id = comanda
    produtos_na_comanda = cursor.execute("SELECT * FROM ProdutoComanda WHERE comanda_id = ?", (comanda_id,))
    for ProdutoComanda in produtos_na_comanda.fetchall():
        id_produtos = ProdutoComanda[1]
        produtos = cursor.execute("SELECT * FROM Produto WHERE id_produto = ?", (id_produtos,))
        for nm_produtos in produtos.fetchall():
            ValorProdutoTotal = nm_produtos[3] * ProdutoComanda[3]
            
            #FROMATAÇÃO DOS VALORES PARA ADEQUAÇÃO NA ENTRADA PARA O DICIONARIO
            valor_format = f'R${nm_produtos[3]}0'
            quantidade_format = f'{ProdutoComanda[3]}xUN'
            codigo_format = f'{nm_produtos[4]})\033[0m'
            valorTotal_format = f'R${ValorProdutoTotal}0'
            valorString = 'VALOR TOTAL:'
            
            #DICIONARIO
            exibicao = {
                codigo_format : [quantidade_format],
                nm_produtos[1] : [valor_format],
                valorString:[valorTotal_format]
            }

            exibicao_df = pd.DataFrame(exibicao)
            print(exibicao_df.to_string(index=False))

            

# SISTEMA DE ESCOLHA DE PRODUTOS
while True:    
    print('-'*50+'\n\033[33mBEM VINDO AO SISTEMA DE LANÇAMENTO DA LANCHE+\033[37m \n'+'-'*50)
    Login()

conexao.commit()
conexao.close()