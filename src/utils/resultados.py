from core.cartao import Cartao
from typing import Optional, Iterable
import requests
import os

# disable warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


BASE_URL = "https://servicebus2.caixa.gov.br/portaldeloterias/api"


class Resultado(Cartao):
    def __init__(self, concurso: int, numeros: Iterable[int] | None = None, bitmap: int | None = None) -> None:
        super().__init__(numeros, bitmap)
        self.concurso = concurso


class Client:
    def __init__(self, loteria: str) -> None:
        self.loteria = loteria

        # setup session
        self.session = requests.Session()
        self.session.verify = False

    @staticmethod
    def get_url(loteria: str, concurso: Optional[int] = None) -> str:
        ret = f"{BASE_URL}/{loteria}"
        if concurso is not None:
            ret = f"{ret}/{concurso}"

        return ret

    @staticmethod
    def get_resultado_json_from_remote(loteria: str, session: requests.Session, concurso: Optional[int] = None) -> dict:
        url = Client.get_url(loteria, concurso)
        response = session.get(url, verify=False)

        response_json = response.json()
        if response.status_code != 200 or 'exceptionMessage' in response_json:
            raise Exception("Erro ao obter o resultado.")

        return response_json

    def get_resultado(self, concurso: Optional[int] = None) -> Resultado:
        response_json = Client.get_resultado_json_from_remote(self.loteria, self.session, concurso)
        return Resultado(response_json['numero'], map(int, response_json['listaDezenas']))


class CachedClient(Client):
    def __init__(self, loteria: str, cache_root_path: str) -> None:
        super().__init__(loteria)
        
        # setup cache
        self.__cache_path = os.path.join(cache_root_path, self.loteria)
        os.makedirs(self.__cache_path, exist_ok=True)
    
    def __get_concurso_cache_path(self, concurso: int):
        return os.path.join(self.__cache_path, self.loteria, f"{concurso}.json")

    def get_resultado(self, concurso: int | None = None) -> Resultado:
        if concurso is None:
            return super().get_resultado(concurso)

        if os.path.exists()

if __name__ == "__main__":
    client = Client('megasena')

    print(client.get_resultado(1))
