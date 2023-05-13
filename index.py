import sqlite3
conexao = sqlite3.connect('bd.sqlite3')
cursor = conexao.cursor()
# Exibe o nome e de todos os produtos
lista_produtos = {"coxinha": 1, "arroz": 2, "feijão": 3, "pao de queijo": 4, "sardinha enlatada": 5}

# FUNÇÕES
def Escolher(num):
    carrinho = {'vazio': 0}
    if escolha == num:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                variavel = produtos
                print(f'Você escolheu \033[33m{produtos}\033[37m')
                quantidade_produto = int(input(F'Me diga quantos \033[33m{produtos}\033[37m você deseja adicionar ao carrinho: '))
    
    for produtos in lista_produtos.keys():
        if carrinho.keys() == produtos:
            print(f'Você já tem \033[33m{produtos}\033[37m no carrinho.')
                
        else:
            carrinho.update({variavel: quantidade_produto})
            print(f'\033[32mProduto(s) adicionado(s) com sucesso!\033[37m')
            
    print(carrinho)


# SISTEMA DE ESCOLHA DE PRODUTOS
while True:
    for produtos, valor in lista_produtos.items(): 
        print(f'{valor}) {produtos.upper()}')

    escolha = int(input("Escolha um produto: "))

    Escolher(escolha)

    desejo = input("Desja parar? 'sim ou não'\n")
    if desejo == 'sim':
        break
    elif desejo == 'não':
        print('Obrigado por preferir nossos produtos!')