Intro
===========================

``ClassevivaAPI`` contiene al suo interno i seguenti moduli:

    - ``classeviva``: modulo principale, contiene tutti i metodi per la gestione della API
    - ``classeviva.collegamenti``: url dell'API
    - ``classeviva.eccezioni``: eccezioni che possono essere sollevate da Classeviva.py
    - ``classeviva.variabili``: costanti e classi per gestire i dati di Classeviva


``classeviva``
===========================
Classeviva è il modulo che contiene le classi per la comunicazione con il sito di Classeviva

Segue l'elenco delle classi pubbliche del modulo classeviva:

- `Utente <#id3>`_: classe che rappresenta un utente
- `ListaUtenti <#id4>`_: classe che rappresenta una lista di utenti


``Utente``
---------------------------

Rappresenta un utente di Classeviva, di tipo Studente [1]_


Classe

    .. code-block:: python

        class Utente(object)


Costruttore

    .. code-block:: python

        def __init__(
            self, 
            id: str, 
            password: str
        ) -> None:

    Parametri:

    - ``id``: username dell'utente
    - ``password``: password dell'utente


Attributi

    - ``self.id: str``: username dell'utente
    - ``password``: password dell'utente
    - ``_sessione: requests.Session``: sessione di comunicazione con l'API
    - ``_dati: dict``: dati dell'utente


Proprietà
    
    Semplici

        - ``biglietto_completo: dict[str, str]`` - `Biglietto <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/ticket.md>`_ [2]_
        - ``biglietto: str`` -  il biglietto, in forma di stringa e non in formato JSON
        - ``secondi_rimasti: int`` - secondi rimasti alla sessione [3]_
        - ``stato: bool`` - comunica se la sessione è ancora attiva
        - ``connesso: bool`` - comunica se la sessione è attiva **senza fare richieste all'API**
        - ``token: str`` - token della sessione
        - ``pagelle: list[dict[str, str]]`` - pagelle in formato JSON [4]_

    Complesse

        - ``dati: dict[str, str]`` - dati dell'utente

        .. code-block:: python

            return {
                "id": self._dati["ident"],
                "nome": self._dati["firstName"],
                "cognome": self._dati["lastName"]
            }

Metodi

    - ``await self.accedi()`` - effettua l'accesso alla sessione [6]_

    .. code-block:: python

        async def accedi(self) -> None:
    
    Eccezioni

        - ``classeviva.eccezioni.PasswordNonValida`` - eccezione generata in caso di errore 422, dato da una password che non combacia con l'username
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore con altro codice HTTP

    - ``await self.documenti()`` - restituisce i documenti dell'utente [5]_

    .. code-block:: python

        async def documenti(self) -> dict[str, list[dict[str, str]]]:
    
    Ritorno

        - ``dict[str, list[dict[str, str]]]`` - i documenti dell'utente in formato JSON [5]_
    
    Eccezioni

        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP

    - ``await self.controlla_documento(documento: str)`` - controlla se il documento è presente

    .. code-block:: python

        async def controlla_documento(self, documento: str) -> bool:

    Parametri

        - ``documento``: il codice hash del documento da controllare
    
    Ritorno

        - ``bool`` - True se il documento è presente, False altrimenti
    
    Eccezioni

        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP
    
    - ``await self.assenze()`` - ottieni gli eventi in cui l'utente ha fatto assenza [7]_

    .. code-block:: python

        async def assenze(self) -> list[dict[str, Any]]:
    
    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi in cui l'utente ha fatto assenza in formato JSON [7]_

    Eccezioni

        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP


Metodi magici

    - ``self.__call__()`` | ``self()`` - connette in modo sincrono l'utente

    .. code-block:: python

        def __call__(self) -> None:
            asyncio.run(self.accedi())


Decoratori

    - ``@classeviva.Utente.connettente`` - passa l'utente alla funzione come primo parametro dopo aver chiamato il metodo ``accedi()``

    .. code-block:: python

        @utente_.connettente
        def foo(x: classeviva.Utente) -> None:
            print(x.dati)
    
    Avvertenze

        - Non funziona con le funzioni asincrone (``async def``) [8]_


Note
===========================

.. [1] Studente, in Classeviva, è un utente il cui identificatore inizia con il carattere 'S'
.. [2] Biglietto, in Classeviva, è una stringa di caratteri, ma non si è ancora capito a cosa serva
.. [3] `Richiesta di stato <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/status.md>`_
.. [4] Sezione "schoolReport" della risposta alla `richiesta di documenti <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/documents.md>`_
.. [5] Sezione "documents" della risposta alla `richiesta di documenti <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/documents.md>`_
.. [6] `Richiesta di accesso <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/login.md>`_
.. [7] `Richiesta di assenze <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Absences/absences.md>`_
.. [8] Alla versione 0.1.0, ma è un miglioramento che verrà aggiunto in futuro