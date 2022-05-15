import asyncio
from datetime import datetime
from typing import Any
import requests

from .collegamenti import collegamenti as c
from .eccezioni import eccezioni as e
from .variabili import variabili as v


class Utente(object):
    
    def __init__(self, id: str, password: str) -> None:
        self.id = id
        self.password = password
        self._sessione = requests.Session()
        self._dati = {}

    def __str__(self) -> str:
        if (self.connesso()):
            return f"<oggetto classeviva.Utente a {id(self)} connesso sin da {self.inizio}>"
        return f"<oggetto classeviva.Utente a {id(self)}>"

    def __del__(self) -> None:
        print(f"{self} è stato ucciso")
        super().__del__()

    def __eq__(self) -> bool:
        return (self.id == self.id) and (self.password == self.password)

    def __hash__(self) -> int:
        return int(str(round(hash(self.id), 8)) + str(round(hash(self.password), 8)))

    def __bool__(self) -> bool:
        return bool(self.id and self.password)

    def __call__(self) -> None:
        asyncio.run(self.accedi())

    async def accedi(self) -> None:
        intestazione = {
            "content-type": "application/json",
            "Z-Dev-ApiKey": "+zorro+",
            "User-Agent": "zorro/1.0"
        }
        dati = {
            "ident": "null",
            "pass": self.password,
            "uid": self.id
        }
        response = self._sessione.post(
            c.Collegamenti.accesso,
            headers=intestazione,
            data=dati
        )
        self._dati = response.json()
        print(self._dati)
        self.inizio = datetime.fromtimestamp(self._dati["release"])
        self.fine = datetime.fromtimestamp(self._dati["expire"])
        self._token = self._dati["token"]

    @property
    def connesso(self) -> bool:
        if (self.inizio is not None):
            return (datetime.now() - self.inizio).total_seconds() < v.TEMPO_CONNESSIONE
        return False

    @property
    def dati(self) -> dict[str, str]:
        return {
            "id": self._dati["ident"],
            "nome": self._dati["fistName"],
            "cognome": self._dati["lastName"]
        }

    @property
    def token(self) -> str:
        if (self._token is None):
            raise e.TokenErrore("Non sei connesso")
        elif (not self.connesso):
            return e.TokenScaduto("Il token è scaduto")
        return self._token