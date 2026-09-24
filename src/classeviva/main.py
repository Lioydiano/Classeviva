from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import NoneType
from typing import Any, Iterable
from collections.abc import Iterable as IterableABC
import requests

from .collegamenti.collegamenti import Collegamenti
from .eccezioni.eccezioni import *
from .variabili.variabili import TEMPO_CONNESSIONE, intestazione, data_inizio_anno, data_fine_anno, valida_date, valida_anno, valida_inizio_fine


class Utente(object):
    
    def __init__(self, id_: str, password: str) -> None:
        self.id = id_
        self._id = id_.lstrip("SGX").rstrip("I")
        self.password = password
        self._sessione = requests.Session()
        self._dati: dict = {}
        self._token: str | None = None

        self.inizio = None
        self.fine = None

        self._sessione.headers.update(intestazione)

    def __str__(self) -> str:
        return f"<oggetto classeviva.Utente a {id(self)}>"

    def __bool__(self) -> bool:
        return all((self.id, self.password))

    def __call__(self) -> None:
        asyncio.run(self.accedi())

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        if isinstance(other, Utente):
            return self._id == other._id and self.password == other.password
        return False
    
    # Decoratore che connette l'utente prima di eseguire la funzione se è necessario
    def connettente(self, funzione):
        def involucro(*args, **kwargs) -> None:
            if not self.connesso:
                self()
            funzione(self, *args, **kwargs)
        return involucro

    async def accedi(self) -> None:
        if self.connesso:
            return None

        # Fai una richiesta alla pagina di accesso per ottenere il cookie `PHPSESSID` (token di sessione)
        self._sessione.headers.update(intestazione)
        response = self._sessione.get(Collegamenti.accesso)
        if response.status_code != 200:
            sollevaErroreHTTP(response=response)

        dati = {"cid": "", "uid": self.id, "pwd": self.password, "pin": "", "target": ""}
        response = self._sessione.post(
            Collegamenti.autenticazione,
            data=dati
        )

        if response.status_code == 200:
            self._dati = response.json()
            self.inizio = datetime.fromisoformat(self._dati["time"])
            self.fine = None # con la nuova API le sessioni non hanno una scadenza (o perlomeno così sembra dalle risposte)
            self._token = self._sessione.cookies.get("PHPSESSID")
            return None
        elif response.status_code == 422:
            raise PasswordNonValida(f"La password di {self} non combacia")
        else:
            sollevaErroreHTTP(response=response)


    async def documenti(self) -> dict[str, list[dict[str, str]]]:
        response = self._sessione.post(
            Collegamenti.documenti.format(self._id),
        )
        if response.status_code == 200:
            return response.json()
        else:
            sollevaErroreHTTP(response=response)

    async def controlla_documento(self, documento: str) -> bool:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.post(
            Collegamenti.controllo_documento.format(self._id, documento)
        )
        if response.status_code == 200:
            return response.json()["document"]["available"]
        else:
             sollevaErroreHTTP(response=response)

    async def assenze(self) -> list[dict[str, Any]]:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.assenze.format(self._id)
        )
        if response.status_code == 200:
            return response.json()["events"]
        else:
             sollevaErroreHTTP(response=response)

    async def assenze_da(self, inizio: str | None = None) -> list[dict[str, Any]]:
        inizio, _ = valida_inizio_fine(inizio, None)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.assenze_da.format(
                self._id, 
                inizio
            )
        )
        if response.status_code == 200:
            return response.json()["events"]
        elif response.status_code == 404:
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if errore.startswith("120"):
                raise FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif errore.startswith("122"):
                raise DataFuoriGamma(f"""
                    La data è fuori dall'anno scolastico
                    Inizio: {inizio}
                """)
            else:
                 sollevaErroreHTTP(response=response)
        else:
             sollevaErroreHTTP(response=response)

    async def assenze_da_a(self, inizio: str | None = None, fine: str | None = None) -> list[dict[str, Any]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.assenze_da_a.format(
                self._id, 
                inizio,
                fine,
            )
        )
        if response.status_code == 200:
            return response.json()["events"]
        elif response.status_code == 404:
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if errore.startswith("120"):
                raise FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif errore.startswith("122"):
                raise DataFuoriGamma(f"""
                    Una data è fuori dall'anno scolastico.
                    OPPURE
                    La data di inizio è successiva a quella di fine.
                    Inizio: {inizio}
                    Fine: {fine}
                """)
            else:
                raise ErroreHTTP404(f"""
                    {response.text}
                    {response.json()}
                """)
        else:
             sollevaErroreHTTP(response=response)

    async def agenda(self) -> list[dict[str, Any]]:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.agenda_da_a.format(
                self._id,
                data_inizio_anno(),
                data_fine_anno()
            )
        )
        if response.status_code == 200:
            return response.json()["agenda"]
        else:
             sollevaErroreHTTP(response=response)

    async def agenda_da_a(self, inizio: str | None = None, fine: str | None = None) -> list[dict[str, Any]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.agenda_da_a.format(
                self._id,
                inizio,
                fine
            )
        )
        if response.status_code == 200:
            return response.json()["agenda"]
        elif response.status_code == 404:
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if errore.startswith("120"):
                raise FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif errore.startswith("122"):
                raise DataFuoriGamma(f"""
                    Una data è fuori dall'anno scolastico.
                    OPPURE
                    La data di inizio è successiva a quella di fine.
                    Inizio: {inizio}
                    Fine: {fine}
                """)
            else: raise ErroreHTTP404(errore)
        else:
             sollevaErroreHTTP(response=response)

    async def agenda_codice_da_a(self, codice: str, inizio: str | None = None, fine: str | None = None) -> list[dict[str, Any]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.agenda_codice_da_a.format(
                self._id, codice,
                inizio,
                fine
            )
        )
        if response.status_code == 200:
            return response.json()["agenda"]
        elif response.status_code == 404:
            errore: str = response.json()["error"]
            # 120:CvvRestApi\/wrong date format
            if errore.startswith("120"):
                raise FormatoNonValido(f"Formato non valido, il parametro dev'essere YYYY-MM-DD")
            # 122:CvvRestApi\/invalid date range
            elif errore.startswith("122"):
                raise DataFuoriGamma(f"""
                    Una data è fuori dall'anno scolastico.
                    OPPURE
                    La data di inizio è successiva a quella di fine.
                    Inizio: {inizio}
                    Fine: {fine}
                """)
            else:
                raise ErroreHTTP404(f"""
                    {response.text}
                    {response.json()}
                """)
        else:
             sollevaErroreHTTP(response=response)

    async def didattica(self) -> list[dict[str, Any]]:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.didattica.format(self._id)
        )
        if response.status_code == 200:
            return response.json()["didacticts"]
        else:
             sollevaErroreHTTP(response=response)

    async def didattica_elemento(self, contenuto: int) -> Any:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.didattica_elemento.format(self._id, contenuto)
        )
        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)

    async def bacheca(self) -> list[dict[str, str | bool | dict[str, str | int]]]:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.bacheca.format(self._id)
        )
        if response.status_code == 200:
            return response.json()["items"]
        else:
             sollevaErroreHTTP(response=response)

    async def bacheca_leggi(self, codice: str, id_: int) -> dict[str, dict[str, Any]]:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.post(
            Collegamenti.bacheca_leggi.format(self._id, codice, id_)
        )
        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)

    async def bacheca_allega(self, id_: int) -> bytes:
        if not self.connesso:
            await self.accedi()

        session = requests.Session()
        session.post(
            url = "https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php?a=aLoginPwd",
            data = {"cid": None, "uid":self._id, "pwd":self.password, "pin": None, "target":None}
        )
        session.post(
            url = "https://web.spaggiari.eu/sif/app/default/bacheca_personale.php",
            data = {"action" : "get_comunicazioni", "cerca": None, "ncna" : 1 , "tipo_com":None}
        ) # Anche se dubito che questo serva
        response = session.get(
            url = Collegamenti.bacheca_allega_esterno.format(id_),
        )
        if response.status_code == 200:
            return response.content
        else:
             sollevaErroreHTTP(response=response)

    async def bacheca_allega_(self, codice: str, id_: int) -> bytes:
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.bacheca_allega.format(self._id, codice, id_)
        )
        if response.status_code == 200:
            return response.content
        else:
             sollevaErroreHTTP(response=response)

    bacheca_allegato = bacheca_allega

    async def lezioni(self) -> list[dict[str, Any]]:
        # Sembra che ritorni sempre una lista vuota
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.lezioni.format(self._id)
        )
        if response.status_code == 200:
            return response.json()["lessons"]
        else:
             sollevaErroreHTTP(response=response)
    
    async def lezioni_giorno(self, giorno: str | None = None) -> list[dict[str, Any]]:
        if giorno is None:
            return await self.lezioni()
        valida_date(giorno)
        
        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.lezioni_giorno.format(self._id, giorno.replace('-', ''))
        )
        if response.status_code == 200:
            return response.json()["lessons"]
        else:
             sollevaErroreHTTP(response=response)
    
    async def lezioni_da_a(self, inizio: str | None = None, fine: str | None = None) -> list[dict[str, Any]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.lezioni_da_a.format(
                self._id,
                inizio,
                fine
            )
        )
        if response.status_code == 200:
            return response.json()["lessons"]
        else:
             sollevaErroreHTTP(response=response)

    async def lezioni_da_a_materia(self, *, inizio: str | None = None, fine: str | None = None, materia: str | None = None) -> list[dict[str, Any]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.lezioni_da_a_materia.format(
                self._id,
                inizio,
                fine,
                materia
            )
        )
        if response.status_code == 200:
            return response.json()["lessons"]
        else:
             sollevaErroreHTTP(response=response)

    async def calendario(self) -> list[dict[str, str | int]]:
        if not self.connesso:
            await self.accedi()
    
        response = self._sessione.get(
            Collegamenti.calendario.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()["calendar"]
        else:
             sollevaErroreHTTP(response=response)

    async def calendario_da_a(self, inizio: str | None = None, fine: str | None = None) -> Any:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()
        response = self._sessione.get(
            Collegamenti.calendario_da_a.format(
                self._id, inizio, fine
            )
        )

        if response.status_code == 200:
            return response.json()["calendar"]
        else:
             sollevaErroreHTTP(response=response)

    async def libri(self) -> dict[str, int | str | dict[str, Any]]:
        if not self.connesso:
            await self.accedi()
    
        response = self._sessione.get(
            Collegamenti.libri.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()["schoolbooks"][0]
        else:
             sollevaErroreHTTP(response=response)

    async def carta(self) -> dict[str, str | int]:
        if not self.connesso:
            await self.accedi()
    
        response = self._sessione.get(
            Collegamenti.carta.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()["card"]
        else:
             sollevaErroreHTTP(response=response)

    async def voti(self, anno: str) -> list[dict[str, str | int | NoneType]]:
        if not self.connesso:
            await self.accedi()

        valida_anno(anno)
        
        response = self._sessione.get(
            Collegamenti.voti.format(self._id, anno)
        )
        
        if response.status_code == 200:
            return response.json()["grades"]
        else:
             sollevaErroreHTTP(response=response)

    async def periodi(self) -> list[dict[str, str | int | bool | NoneType]]:
        if not self.connesso:
            await self.accedi()
        
        response = self._sessione.get(
            Collegamenti.periodi.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()["periods"]
        else:
             sollevaErroreHTTP(response=response)

    async def materie(self) -> list[dict[str, str | int | list[dict[str, str]]]]:
        if not self.connesso:
            await self.accedi()
        
        response = self._sessione.get(
            Collegamenti.materie.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()["subjects"]
        else:
             sollevaErroreHTTP(response=response)

    async def note(self) -> dict[str, list[dict[str, str | int | bool]]]:
        if not self.connesso:
            await self.accedi()
        
        response = self._sessione.get(
            Collegamenti.note.format(self._id)
        )
        
        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)

    async def leggi_nota(self, tipo: str, id_: int) -> str:
        if not self.connesso:
            await self.accedi()

        response = self._sessione.post(
            Collegamenti.leggi_nota.format(self._id, tipo, id_)
        )

        if response.status_code == 200:
            return response.json()["event"]["evtText"]
        elif response.status_code == 404:
            errore: str = response.json()["error"]
            # 130:CvvRestApi\/invalid event-id
            if errore.startswith('130'):
                raise ParametroNonValido(f"Nota con ID {id_} non trovata")
            # 102:CvvRestApi\/wrong uri
            elif errore.startswith('102'):
                raise CategoriaNonPresente(f"Categoria di nota {tipo} non trovata")
            else:
                 sollevaErroreHTTP(response=response)
        else:
             sollevaErroreHTTP(response=response)

    async def panoramica(self) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:

        if not self.connesso:
            await self.accedi()

        response = self._sessione.get(
            Collegamenti.panoramica_da_a.format(
                self._id,
                data_inizio_anno(),
                data_fine_anno()
            )
        )

        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)

    async def panoramica_completa(self, year: str) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:

        if not self.connesso:
            await self.accedi()

        valida_anno(year)

        response = self._sessione.get(
            Collegamenti.panoramica_completa_da_a.format(
                self._id,
                year,
                data_inizio_anno(),
                data_fine_anno()
            )
        )

        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)


    async def panoramica_da_a(self, inizio: str | None = None, fine: str | None = None) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()

        response = self._sessione.get(
            Collegamenti.panoramica_da_a.format(
                self._id,
                inizio,
                fine
            )
        )

        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)

    async def panoramica_completa_da_a(self, inizio: str | None = None, fine: str | None = None) -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
        inizio, fine = valida_inizio_fine(inizio, fine)

        if not self.connesso:
            await self.accedi()

        response = self._sessione.get(
            Collegamenti.panoramica_completa_da_a.format(
                self._id,
                inizio.strftime("%y"),
                inizio.strftime("%Y%m%d"),
                fine.strftime("%Y%m%d"),
            )
        )

        if response.status_code == 200:
            return response.json()
        else:
             sollevaErroreHTTP(response=response)


    @property
    def biglietto_completo(self) -> dict[str, str]:
        response = self._sessione.get(
            Collegamenti.biglietto
        )
        if response.status_code != 200:
             sollevaErroreHTTP(response=response)
        try:
            return response.json()
        except Exception as e_:
            print(e_)

    @property
    def biglietto(self) -> str:
        if not self.biglietto_completo:
            raise SenzaDati(f"{self.__class__.__name__}.biglietto non esiste.")
        
        try:
            return self.biglietto_completo["ticket"]
        except Exception as e_:
            print(e_)

    @property
    def connesso(self) -> bool:
        if hasattr(self, "inizio"):
            passati = (datetime.now(timezone.utc) - self.inizio).total_seconds()
            return passati < TEMPO_CONNESSIONE
        return False

    @property
    def dati(self) -> dict[str, str]:
        try:
            return {
                chiave: valore for chiave, valore in self._dati.items()
                if chiave in {"ident", "firstName", "lastName"}
            }
        except KeyError:
            raise SenzaDati(f"{self} non ha i dati sufficienti per questa proprietà")

    @property
    def pagelle(self) -> list[dict[str, str]]:
        documenti_ = asyncio.run(self.documenti())
        if not documenti_:
            raise ValueError(f"{self} non ha i dati sufficienti per questa proprietà (forse le pagelle non sono ancora uscite)")

        try:
            return [{
                chiave: valore for chiave, valore in documento_.items() 
                if chiave in {"desc", "confirmLink", "viewLink"}
            } for documento_ in documenti_["schoolReports"]]
        except KeyError:
            raise SenzaDati(f"{self} non ha i dati sufficienti per questa proprietà (forse le pagelle non sono ancora uscite)")

    @property
    def token(self) -> str:
        if self._token is None:
            raise TokenErrore("Non sei connesso")
        elif not self.connesso:
            raise TokenScaduto("Il token è scaduto")
        return self._token


class ListaUtenti(set[Utente]):

    def __init__(self, utenti: Iterable[Utente] | None) -> None:
        super().__init__()

        if utenti:
            for utente in utenti:
                if isinstance(utente, Utente):
                    self.add(utente)

    def __str__(self) -> str:
        return f"<oggetto classeviva.ListaUtenti a {id(self)}>"

    def __call__(self) -> None:
        asyncio.run(self.accedi())

    def __add__(self, oggetto) -> None:
        if isinstance(oggetto, Utente):
            self.aggiungi(oggetto)
        elif isinstance(oggetto, IterableABC):
            for oggetto_ in oggetto:
                self.aggiungi(oggetto_)
        else:
            raise TypeError(f"{oggetto} non è un oggetto valido")

    def __contains__(self, other: Any) -> bool:
        if isinstance(other, Utente):
            for utente in self:
                if utente == other:
                    return True
        return False

    def aggiungi(self, utente: Utente) -> bool:
        if isinstance(utente, Utente) and utente not in self:
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
        return {utente for utente in self if utente.connesso}

    @property
    def non_connessi(self) -> set[Utente]:
        return {utente for utente in self if not utente.connesso}
