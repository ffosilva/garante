import requests
import threading
import os
import sys
import json
import random

from core.cartao import Cartao
from requests.adapters import HTTPAdapter
from typing import Iterable, Optional
from urllib3.util import Retry
from urllib3.exceptions import InsecureRequestWarning
 
# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Resultado(Cartao):
    def __init__(self, loteria: str, concurso: int, numeros: Iterable[int] | None = None, bitmap: int | None = None) -> None:
        super().__init__(numeros, bitmap)
        self.loteria = loteria
        self.concurso = concurso


class SessionHandler:
    def __init__(self, retries=5, backoff_factor=0.3, status_forcelist: Iterable[int] = frozenset([500, 502, 504]), verify = False) -> None:
        self.session = None
        self.initialized = False

        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.verify = verify
        
        self.lock = threading.Lock()


    def __del__(self):
        if self.initialized:
            self.session.close()


    def get_session(self):
        if self.initialized:
            return self.session

        try:
            self.lock.acquire()
            
            if self.initialized:
                self.lock.release()
                return self.session
            
            self.session = requests.Session()
            self.session.verify = self.verify
            retry = Retry(total=self.retries, read=self.retries, connect=self.retries, status=self.retries,
                                backoff_factor=self.backoff_factor,
                                status_forcelist=self.status_forcelist,
                                allowed_methods=Retry.DEFAULT_ALLOWED_METHODS)
            adapter = HTTPAdapter(max_retries=retry)

            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            self.initialized = True
        finally:
            self.lock.release()

        return self.session


class ResultadosClient:
    def __init__(self, loteria: str):
        self.loteria = loteria
        self.session_hander = SessionHandler()

    def _process_response(self, response_json):
        dezenas = list(map(int, response_json["dezenasSorteadasOrdemSorteio"]))
        concurso = response_json["numero"]
        
        return Resultado(self.loteria, concurso, dezenas)

    def _get_resultado_from_remote(self, concurso: str | None) -> dict:
        concurso_str = ""
        if concurso is not None:
            concurso_str = str(concurso)

        resultado_url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{self.loteria}/{concurso_str}"
        headers = {"Accept": "application/json"}

        try:
            session = self.session_hander.get_session()
            response = session.get(resultado_url, headers=headers)

            if response.status_code == 200 and 'dezenasSorteadasOrdemSorteio' in response.json():
                return response.json()
        except:
            raise Exception(f"Não foi possível obter o resultado. [Loteria = '{self.loteria}', Concurso = '{concurso_str}]")


    def get_resultado(self, concurso: int | None = None) -> Resultado:
        response = self._get_resultado_from_remote(concurso)
        
        return self._process_response(response)


class CachedResultadosClient(ResultadosClient):
    __DEFAULT_CACHE_DIR = "cache"

    @staticmethod
    def __get_cache_dir(cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = os.environ.get("GARANTE_CACHE_DIR", CachedResultadosClient.__DEFAULT_CACHE_DIR)

        return cache_dir
    

    def __init__(self, loteria: str, cache_dir: Optional[str] = None):
        super().__init__(loteria)

        cache_dir = CachedResultadosClient.__get_cache_dir(cache_dir)

        self.cache_dir = os.path.join(cache_dir, loteria)
        os.makedirs(self.cache_dir, exist_ok = True)
    
    def get_resultado(self, concurso: int | None = None) -> Resultado:
        if concurso is None:
            return super().get_resultado()

        concurso_path = os.path.join(self.cache_dir, f"{concurso}.json")
        if os.path.exists(concurso_path):
            with open(concurso_path, 'r') as concurso_fp:
                return self._process_response(json.load(concurso_fp))
        else:
            response = self._get_resultado_from_remote(concurso)
            with open(concurso_path, 'w') as concurso_fp:
                json.dump(response, concurso_fp)
            
            return self._process_response(response)


def gerar_jogo(quantidade_dezenas, maior_dezena):
    todas_dezenas = list(range(1, maior_dezena + 1))
    random.shuffle(todas_dezenas)

    return todas_dezenas[:quantidade_dezenas]


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: python {sys.argv[0]} <nome da loteria>")
        exit(1)

    nome_loteria = sys.argv[1]
    client = CachedResultadosClient(nome_loteria)

    ultimo_resultado = client.get_resultado()
    numero_concurso = ultimo_resultado.concurso

    print(f"Loteria: {nome_loteria} - Último concurso: {numero_concurso}")

    resultados = []
    for i in range(1, numero_concurso + 1):
        resultado = Cartao(list(map(int, client.get_resultado(i).iterate())))
        resultados.append(resultado)
