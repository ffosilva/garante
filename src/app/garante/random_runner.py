import sys
import os
from garante import main

total_dezenas = 10
tamanho_aposta = 6
garante = 4
acertando = 4
caminho_saida = "./"
seed = None
ustdout = open(os.devnull, 'w')

if __name__ == "__main__":
    main(total_dezenas, tamanho_aposta, garante, acertando, caminho_saida, None, ustdout, False)
    while True:
        main(total_dezenas, tamanho_aposta, garante, acertando, caminho_saida, None, ustdout, True)
