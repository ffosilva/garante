from core.cartao import Cartao
from app.garante.grupos import gerar_combinacoes as gerar_combinacoes_grupos

quantidade_grupos = 6
dezenas_por_grupo = 4

todas_combinacoes_generator = gerar_combinacoes_grupos(quantidade_grupos, dezenas_por_grupo)

escolhidos: set[Cartao] = set([next(todas_combinacoes_generator)])

garante = 4

for cartao in todas_combinacoes_generator:
    encontrado = True
    for escolhido in escolhidos:
        if cartao.qtde_acertos(escolhido) > (garante - 1):
            encontrado = False
            break
    
    if encontrado:
        escolhidos.add(cartao)

print(len(escolhidos))


todas_combinacoes_generator = gerar_combinacoes_grupos(quantidade_grupos, dezenas_por_grupo, 4)
print(len(list(todas_combinacoes_generator)))

todas_combinacoes_generator = gerar_combinacoes_grupos(quantidade_grupos, dezenas_por_grupo, 4)


for combinacao in todas_combinacoes_generator:
    for cartao in escolhidos:
        if cartao.qtde_acertos(combinacao) >= 3:
            print("Encontrado!")
            break
        print(f"Cartao nao encontrado!! {combinacao}")
        exit(1)
