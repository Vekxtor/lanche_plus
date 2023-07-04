#Mensagens (prints) de carregamento deve ficar em VERDE
#Mensagens de falha em VERMELHO
#Nome de operadores em LARANJA
import pandas as pd
import sqlite3
from datetime import datetime
conexao = sqlite3.connect('bank\BancoProdutos.sqlite3')
cursor = conexao.cursor()
#PEGANDO O HORÁRIO DO AGORA...
agora = datetime.now()
horario_atual = agora.strftime("%H:%M:%S")
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

def Login(): #LOGIN DO USUARIO/funcionario
    usuario = int(input("DIGITE SUA SENHA: "))
    cursor.execute("SELECT senha, nm_usuario, id_usuario FROM Usuario WHERE senha = ?", (usuario,))
    print('\033[32mCARREGANDO INFORMAÇÕES...\033[37m')

    login = cursor.fetchone()  # Recupera apenas um resultado

    if login is not None and usuario == login[0]:
        id_usuario = login[2]
        print(f'OPERADOR: \033[38;5;208m{login[1]}\033[37m')
        
        escolha = input('(1) GERENCIAR COMANDAS\n(2) DAR BAIXA EM COMANDA\n')
        if escolha == '1':
            Comanda(id_usuario)
        if escolha == '2':
            Fechar(id_usuario)
    else:
        print('\033[91mSENHA INVÁLIDA\033[0m')

def Comanda(id_usuario): #PEDINDO COMANDA PARA INICIAR AS OPERAÇÕES DESEJADAS

    num_comanda = int(input("DIGITE O NUMERO DA COMANDA: ")) #COMANDA DE MANIPULÇÃO DO OPERADOR
    
    #VERIFICANDO SE HÁ PRODUTOS NA COMANDA
    sql = f'SELECT COUNT(pc.comanda_id) FROM ProdutoComanda pc JOIN Comanda c on c.id_comanda = pc.comanda_id WHERE c.nmr_comanda = ?'
    for res in cursor.execute(sql, [num_comanda]):
        if int(res[0]) > 0:
            VerifComanda = True
        else:
            VerifComanda = False

    if VerifComanda == True:
        sql = 'SELECT c.id_comanda FROM Comanda c WHERE c.nmr_comanda = ?'
        valores = [num_comanda]
        
        for res in cursor.execute(sql, valores):
            idProdutoComanda = res[0]

        sql = f'SELECT c.nmr_comanda, c.nm_comanda, c.dt_aberto_comanda, u.nm_usuario FROM Comanda c JOIN Usuario u ON c.usuario_id = u.id_usuario  WHERE C.nmr_comanda = ?'
        valores = [num_comanda]
        
        for res in cursor.execute(sql, valores):
            print('='*50)
            print(f'FICHA {res[0]} | MESA {res[1]} | ABERTO {res[2]} P/ {res[3]}')
        
        sql = 'SELECT p.cd_produto, p.nm_produto, pc.qtd_produto, pc.lancamento, p.vlr_produto FROM ProdutoComanda pc JOIN Produto p ON p.id_produto = pc.produto_id JOIN Comanda c ON c.id_comanda = pc.comanda_id WHERE pc.comanda_id = ?'
        valores = [idProdutoComanda]

        vlrtotal = 0
        for res in cursor.execute(sql, valores):
            qtd = res[2] 
            vlr = res[4]
            qtdvlr = qtd * vlr
            vlrtotal += qtdvlr
            print(f'{res[0]}) {res[1]}\nR$ {res[4]}0 {res[2]}xUN R$ {qtdvlr}0 | {res[3]}\n')
        print(f'VALOR TOTAL DA COMANDA: R$ {vlrtotal}0')
        print('='*50)
        Lancamento(num_comanda)

    elif VerifComanda == False:
        print('COMANDA VAZIA!')
        CriarComanda(num_comanda, id_usuario)

def CriarComanda(comanda, id_usuario):
    NmrMesa = int(input('DIGITE O NÚMERO DA MESA: '))
    
    cursor.execute("INSERT INTO Comanda (nmr_comanda, nm_comanda, dt_aberto_comanda, usuario_id) VALUES (?, ?, ?, ?)", (comanda, NmrMesa, horario_atual, id_usuario,))
    conexao.commit()

    Lancamento(comanda) #ENVIANDO PARA A FUNÇÃO DE LANÇAMENTO QUAL É O NÚMERO DA COMANDA QUE FOI DIGITADO PELO USUARIO

def Lancamento(comanda):
    
    cursor.execute("SELECT id_comanda, nmr_comanda FROM Comanda WHERE nmr_comanda = ?", (comanda,))
    idComanda = cursor.fetchone()

    if idComanda is not None and idComanda[1] == comanda:
        FKComanda = idComanda[0]

        stop = False
        while stop == False:
            codProduto = int(input("DIGITE O CÓDIGO DO PRODUTO:\n"))
            quantidade = int(input("DIGITE A QUANTIDADE DESEJADA: "))

            sql = f'SELECT p.cd_produto, p.nm_produto FROM Produto p WHERE p.cd_produto = ?'
            for res in cursor.execute(sql, [codProduto]):
                proceder = input(f'{res[0]} | VOCÊ DESEJA LANÇAR {quantidade}xUND de {res[1]}? (s/n)\n')
                if proceder == 's':
                    #DESCOBRINDO QUAL É O ID_PRODUTO
                    cursor.execute("SELECT id_produto, cd_produto, nm_produto FROM Produto WHERE cd_produto = ?", (codProduto,))
                    idProduto = cursor.fetchone()
                    if idProduto is not None and idProduto[1] == codProduto:
                        cursor.execute("INSERT INTO ProdutoComanda (produto_id, comanda_id, qtd_produto, lancamento) VALUES(?, ?, ?, ?) ", (idProduto[0], FKComanda, quantidade, horario_atual))
                        conexao.commit()

                        stop_usu = input("DESEJA CONTINUAR LANCANDO? (s/n)\n")
                else:
                    stop = False

            
                if stop_usu == 's':
                    stop = False
                else:
                    stop = True

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

def Fechar(id_usuario):
    print('='*50)
    print("\033[1;32mINICIALIZANDO MAPA...\033[0m")
    sql = 'SELECT c.nmr_comanda FROM Comanda c'
    for res in cursor.execute(sql):
        print(f' {res[0]}')
        print('='*5)

    NMRComanda = input()
    print("\033[1;32mCARREGANDO COMANDA...\033[0m")
    sql = f'SELECT c.nmr_comanda, c.nm_comanda, c.dt_aberto_comanda, u.nm_usuario FROM Comanda c JOIN Usuario u ON c.usuario_id = u.id_usuario WHERE c.nmr_comanda = ? '
    for res in cursor.execute(sql, [NMRComanda]):
        print(f'\033[33mMESA: \033[37m{res[1]} \033[33mABERTO EM: \033[37m{res[2]}\n\033[33mCOMANDA: \033[37m{res[0]} \033[33mOPERADOR: \033[37m{res[3]}')

    print('\033[34mler mais...\033[37m')
    input()
    sql = f'SELECT pc.qtd_produto, pc.lancamento, p.nm_produto, p.vlr_produto, p.cd_produto FROM ProdutoComanda pc JOIN Comanda c ON c.id_comanda = pc.comanda_id JOIN Produto p ON p.id_produto = pc.produto_id WHERE c.nmr_comanda = ?'
    vlrTotal = 0 #CALCULANDO O VALOR DOS PRODUTOS REPETIDOS NA COMANDA
    informacoes = ''
    for res in cursor.execute(sql, [NMRComanda]):
        qtdvalor = res[0] * res[3]
        vlrTotal += qtdvalor
        linha = '='*50
        informacoes += f'\n{res[4]}) {res[2]} R$ {res[3]}0\nLANÇAMENTO ÀS {res[1]}\n{res[0]}xUN R$ {qtdvalor}0\n{linha}'
    print("\033[1;32mCARREGANDO PRODUTOS...\033[0m")
    print(informacoes)
    print('\n')
    print("\033[33mPRECIONE A TECLA 'ENTER' PARA PROCEGUIR...\033[0m")
    input()
    fmtVlrTotal = "{:.2f}".format(vlrTotal)
    print(f'O VALOR TOTAL DA COMANDA É {fmtVlrTotal}')
    pagamento = int(input('VALOR PAGO PELO CLIENTE\n'))
    if pagamento < vlrTotal:
        falta = vlrTotal - pagamento
        print(f'\033[31m{("{:.2f}".format(falta))}\033[37m')
        resto = int(input())
        if resto > falta:
            troco = falta - resto
            print(("{:.2f}".format(troco)))
    if pagamento > vlrTotal:
        troco = pagamento - vlrTotal
        print(("{:.2f}".format(troco)))

    print("\033[33mPARA FECHAR COMANDA 'ENTER'...\033[0m")
    input()

    #CARREGANDO INFORMAÇÕES QUE SERÃO SALVAS NA TABELA HISTORICO COM TEXTO...
    sql = 'SELECT c.nmr_comanda, c.nm_comanda, c.dt_aberto_comanda, u.nm_usuario FROM Comanda c JOIN Usuario u ON u.id_usuario = c.usuario_id WHERE c.nmr_comanda = ?'
    for res in cursor.execute(sql, [NMRComanda]):
        H_nmrComanda = res[0]
        H_nmMesa = res[1]
        H_hrAbriu = res[2]
        H_opAbriu = res[3]

    H_descricao = informacoes
    H_vlrTotal = ("{:.2f}".format(vlrTotal))
    H_hrFechou = horario_atual
    
    sql = 'SELECT u.nm_usuario FROM Usuario u WHERE u.id_usuario = ?'
    for res in cursor.execute(sql, [id_usuario]):
        H_opFechou = res[0]
    
    valores = [H_nmrComanda, H_nmMesa, H_hrAbriu, H_opAbriu, H_descricao, H_vlrTotal, H_hrFechou, H_opFechou]
    #ENIANDO INFORMAÇÕES CARREGADAS...
    sql = '''
        INSERT INTO Historico
            (nmr_comanda, nm_mesa, hr_abriu, op_abriu, descricao, vlr_total, hr_fechou, op_fechou)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.execute(sql, valores)

    #DESCOBRINDO O ID DA COMANDA
    sql = 'SELECT c.id_comanda FROM Comanda c WHERE c.nmr_comanda = ?'
    for res in cursor.execute(sql, [NMRComanda]):
        idComanda = res[0]

    #LIBERANDO COMANDA DO BANCO DE DADOS...
    cursor.execute('DELETE FROM Comanda WHERE id_comanda= ?', [idComanda])
    cursor.execute('DELETE FROM ProdutoComanda WHERE id_ProdutoComanda=?', [idComanda])


# SISTEMA DE ESCOLHA DE PRODUTOS
  
print('-'*50+'\n\033[33mBEM VINDO AO SISTEMA DE LANÇAMENTO DA LANCHE+\033[37m \n'+'-'*50)
Login()

conexao.commit()
conexao.close()