# Exibe o nome e de todos os produtos
lista_produtos = {"coxinha": 1, "arroz": 2, "feijão": 3, "pao de queijo": 4, "sardinha enlatada": 5}

for produtos, valor in lista_produtos.items(): 
    print(f'{valor}) {produtos.upper()}')

# SISTEMA DE ESCOLHA DE PRODUTOS
while True:
    escolha = int(input("Escolha um produto: "))

    if escolha == 1:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print("Você escolheu a Coxinha")
    if escolha == 2:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print("Você escolheu o Arroz")
    if escolha == 3:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print("Você escolheu o Feijão")
    if escolha == 4:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print("Você escolheu o Pão de Queijo")
    if escolha == 5:
        for produtos, valor in lista_produtos.items():
            if escolha == valor:
                print("Você escolheu a Sardinha Enlatada")

    break