from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Any, Iterable
from collections.abc import Iterable as IterableABC
import requests

from .collegamenti import collegamenti as c
from .eccezioni import eccezioni as e
from .variabili import variabili as v


class Utente(object):
    
    def __init__(self, id: str, password: str) -> None:
        self.id = id
        self.password = password
        self._sessione = requests.Session()
        self._dati: dict = {}

    def __str__(self) -> str:
        return f"<oggetto classeviva.Utente a {id(self)}>"

    def __bool__(self) -> bool:
        return self.id and self.password

    def __call__(self) -> None:
        asyncio.run(self.accedi())

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        if (isinstance(other, Utente)):
            return (self.id == other.id and self.password == other.password)
        return False

    async def accedi(self) -> None:
        if (self.connesso):
            return
        dati = f'{{"ident": null, "pass": "{self.password}", "uid": "{self.id}"}}'
        response = self._sessione.post(
            c.Collegamenti.accesso,
            headers=v.intestazione,
            data=dati
        )
        if (response.status_code == 200):
            self._dati = response.json()
            self.inizio = datetime.fromisoformat(self._dati["release"])
            self.fine = datetime.fromisoformat(self._dati["expire"])
            self._token = self._dati["token"]
        elif (response.status_code == 422):
            raise e.PasswordNonValida(f"La password di {self} non combacia")
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/documents.md
    async def documenti(self) -> dict[str, list[dict[str, str]]]:
        if (not self.connesso):
            await self.accedi()
        response = self._sessione.post(
            c.Collegamenti.documenti.format(self.id.removeprefix("S")),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/check%20document.md
    async def controlla_documento(self, documento: str) -> bool:
        if (not self.connesso):
            await self.accedi()
        response = self._sessione.post(
            c.Collegamenti.controllo_documento.format(self.id.removeprefix("S"), documento),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()["document"]["available"]
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Absences/absences.md
    async def assenze(self) -> list[dict[str, Any]]:
        if (not self.connesso):
            await self.accedi()
        response = self._sessione.get(
            c.Collegamenti.assenze.format(self.id.removeprefix("S")),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()["events"]
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Absences/from.md
    async def assenze_da(self, inizio: str=None) -> list[dict[str, Any]]:
        if (inizio is None):
            return await self.assenze()
        v.valida_date(inizio)

        if (not self.connesso):
            await self.accedi()
        response = self._sessione.get(
            c.Collegamenti.assenze_da.format(
                self.id.removeprefix("S"), 
                inizio.replace("-", "")
            ),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()["events"]
        elif (response.status_code == 404):
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if (errore.startswith("120")):
                raise e.FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif (errore.startswith("122")):
                raise e.DataFuoriGamma(f"""
                    La data è fuori dall'anno scolastico
                    Inizio: {inizio}
                """)
            else:
                raise e.ErroreHTTP(f"""
                    Richiesta non corretta, codice {response.status_code}
                    {response.text}
                    {response.json()}
                """)
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Absences/from_to.md
    async def assenze_da_a(self, inizio: str=None, fine: str=None) -> list[dict[str, Any]]:
        if (inizio is None):
            return await self.assenze()
        elif (fine is None):
            return await self.assenze_da(inizio)
        v.valida_date(inizio, fine)

        if (not self.connesso):
            await self.accedi()
        response = self._sessione.get(
            c.Collegamenti.assenze_da.format(
                self.id.removeprefix("S"), 
                inizio.replace('-', ''), 
                fine.replace('-', '')
            ),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()["events"]
        elif (response.status_code == 404):
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if (errore.startswith("120")):
                raise e.FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif (errore.startswith("122")):
                raise e.DataFuoriGamma(f"""
                    Una data è fuori dall'anno scolastico.
                    OPPURE
                    La data di inizio è successiva a quella di fine.
                    Inizio: {inizio}
                    Fine: {fine}
                """)
            else:
                raise e.ErroreHTTP(f"""
                    Richiesta non corretta, codice {response.status_code}
                    {response.text}
                    {response.json()}
                """)
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    async def agenda(self) -> Any:
        if (not self.connesso):
            await self.accedi()
        response = self._sessione.get(
            c.Collegamenti.agenda_da_a.format(
                self.id.removeprefix("S"),
                v.data_inizio_anno(),
                v.data_fine_anno()
            ),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    async def agenda_da_a(self, inizio: str, fine: str) -> Any:
        if (None in {inizio, fine}):
            return await self.agenda()
        v.valida_date(inizio, fine)

        if (not self.connesso):
            await self.accedi()
        response = self._sessione.get(
            c.Collegamenti.agenda_da_a.format(
                self.id.removeprefix("S"),
                inizio.replace('-', ''), 
                fine.replace('-', '')
            ),
            headers=self.__intestazione()
        )
        if (response.status_code == 200):
            return response.json()
        else:
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)

    def __intestazione(self) -> dict[str, str]:
        intestazione = v.intestazione.copy()
        if (not hasattr(self, "_token")):
            raise e.TokenNonPresente("Token non presente")
        intestazione["Z-Auth-Token"] = self._token
        return intestazione

    # Decoratore che connette l'utente prima di eseguire la funzione se è necessario
    def connettente(self, funzione):
        def involucro(*args, **kwargs) -> None:
            if (not self.connesso):
                self()
            funzione(self, *args, **kwargs)
        return involucro

    @property
    def biglietto_completo(self) -> dict[str, str]:
        response = self._sessione.get(
            c.Collegamenti.biglietto,
            headers=self.__intestazione()
        )
        if (response.status_code != 200):
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)
        try:
            return response.json()
        except Exception as e_:
            print(e_)

    @property
    def biglietto(self) -> str:
        return self.biglietto_completo["ticket"]

    @property
    def secondi_rimasti(self) -> int:
        response = self._sessione.get(
            c.Collegamenti.stato,
            headers=self.__intestazione()
        )
        if (response.status_code != 200):
            raise e.ErroreHTTP(f"""
                Richiesta non corretta, codice {response.status_code}
                {response.text}
                {response.json()}
            """)
        try:
            return response.json()["status"]["remains"]
        except Exception as e_:
            print(e_)

    # https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/status.md
    @property
    def stato(self) -> bool:
        return self._sessione.get(
            c.Collegamenti.stato,
            headers=self.__intestazione()
        ).status_code == 200 # Token ancora valido

    @property
    def connesso(self) -> bool:
        if (hasattr(self, "inizio")):
            passati = (datetime.now(timezone.utc) - self.inizio).total_seconds()
            return passati < v.TEMPO_CONNESSIONE
        return False

    @property
    def dati(self) -> dict[str, str]:
        try:
            return {
                "id": self._dati["ident"],
                "nome": self._dati["firstName"],
                "cognome": self._dati["lastName"]
            }
        except KeyError:
            raise e.SenzaDati(f"{self} non ha i dati sufficienti per questa proprietà")

    @property
    def pagelle(self) -> list[dict[str, str]]:
        documenti_ = asyncio.run(self.documenti())
        try:
            return [{
                "descrizione": documento_["desc"],
                "conferma": documento_["confirmLink"],
                "lettura": documento_["viewLink"]
            } for documento_ in documenti_["schoolReports"]]
        except KeyError:
            raise e.SenzaDati(f"{self} non ha i dati sufficienti per questa proprietà")

    @property
    def token(self) -> str:
        if (self._token is None):
            raise e.TokenErrore("Non sei connesso")
        elif (not self.connesso):
            raise e.TokenScaduto("Il token è scaduto")
        return self._token


class ListaUtenti(set[Utente]):

    def __init__(self, utenti: Iterable[Utente]) -> None:
        for utente in utenti:
            if (isinstance(utente, Utente)):
                self.add(utente)
        self.__riduci()

    def __str__(self) -> str:
        return f"<oggetto classeviva.ListaUtenti a {id(self)}>"

    def __call__(self) -> None:
        asyncio.run(self.accedi())

    def __add__(self, oggetto) -> ListaUtenti:
        if (isinstance(oggetto, Utente)):
            self.aggiungi(oggetto)
        elif (isinstance(oggetto, IterableABC)):
            for oggetto_ in oggetto:
                self.aggiungi(oggetto_)
        else:
            raise TypeError(f"{oggetto} non è un oggetto valido")

    def __contains__(self, utente: Utente) -> bool:
        if (isinstance(utente, Utente)):
            for utentino in self:
                if (utente == utentino):
                    return True
        return False

    def __riduci(self) -> None:
        for utente in self:
            copia = self.copy()
            copia.remove(utente)
            for utentino in copia:
                if (utente == utentino):
                    self.remove(utentino)

    def aggiungi(self, utente: Utente) -> bool:
        if (isinstance(utente, Utente) and utente not in self):
            self.add(utente)
            return True
        return False

    async def accedi(self) -> None:
        await asyncio.gather(*[utente.accedi() for utente in self.non_connessi])

    def iterante(self, funzione):
        def involucro(*args, **kwargs) -> None:
            for elemento in self:
                try:
                    funzione(elemento, *args, **kwargs)
                except Exception as e_:
                    print(e_)
        return involucro

    @property
    def connessi(self) -> set[Utente]:
        return {utente for utente in self if (utente.connesso)}

    @property
    def non_connessi(self) -> set[Utente]:
        return {utente for utente in self if (not utente.connesso)}