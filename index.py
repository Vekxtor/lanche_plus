# Exibe o nome e de todos os produtos
lista_produtos = {"coxinha": 1, "arroz": 2, "feijão": 3, "pao de queijo": 4, "sardinha enlatada": 5}

for produtos, valor in lista_produtos.items(): 
    print(f'{valor}) {produtos.upper()}')

# FUNÇÕES
def Escolher(num):
    if escolha == num:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print(f'Você escolheu \033[33m{produtos}\033[37m')

# SISTEMA DE ESCOLHA DE PRODUTOS
while True:
    escolha = int(input("Escolha um produto: "))
    carrinho = {}

    Escolher(escolha)

    break