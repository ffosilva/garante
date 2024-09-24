import random

from core.cartao import Cartao

class Globo():
    def __init__(self, maior_dezena) -> None:
        self.__maior_dezena = maior_dezena
        self.__globo: list[int] = list()
        self.reinicia_globo()

    def reinicia_globo(self) -> None:
        self.__globo.extend([i for i in range(1, self.__maior_dezena + 1)])
        random.shuffle(self.__globo)

    def pegar_dezena(self) -> int:
        if len(self.__globo) <= 0:
            self.reinicia_globo()
        
        return self.__globo.pop()

    def devolver_dezena(self, dezena):
        self.__globo.insert(1, dezena)
        random.shuffle(self.__globo)

    def gerar_cartao(self, tamanho_cartao) -> Cartao:
        dezenas_cartao: set[int] = set()
        while len(dezenas_cartao) < tamanho_cartao:
            dezena = self.pegar_dezena()
            if dezena in dezenas_cartao:
                self.devolver_dezena(dezena)
                continue

            dezenas_cartao.add(dezena)
        
        return Cartao(dezenas_cartao)

if __name__ == "__main__":
    globo = Globo(25)

    for i in range(100):
        print(globo.gerar_cartao(15))
