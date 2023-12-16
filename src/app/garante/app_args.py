from typing import Optional

class AppArgs:
    total_dezenas: int = None
    tamanho_aposta: int = None
    garante: int = None
    acertando: int = None
    caminho_saida: str = None
    seed: Optional[int] = None

    def __init__(self, total_dezenas: int, tamanho_aposta: int, garante: int, acertando: int, caminho_saida: str, seed: Optional[int]) -> None:
        self.total_dezenas = total_dezenas
        self.tamanho_aposta = tamanho_aposta
        self.garante = garante
        self.acertando = acertando
        self.caminho_saida = caminho_saida
        self.seed = seed
        
