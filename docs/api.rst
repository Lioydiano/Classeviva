Intro
===========================

``Classeviva.py`` contiene al suo interno i seguenti moduli:

    - ``classeviva``: modulo principale, contiene tutti i metodi per la gestione della API
    - ``classeviva.collegamenti``: URL dell'API
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
    - ``password: str``: password dell'utente
    - ``_sessione: requests.Session``: sessione di comunicazione con l'API
    - ``_dati: dict``: dati dell'utente


Proprietà
    
    Semplici

        - ``biglietto_completo: dict[str, str]`` - `Biglietto <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/ticket.md>`_ [2]_
        - ``biglietto: str`` -  il biglietto, in forma di stringa e non in formato JSON [JSON]_
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


    - ``await self.assenze_da(inizio: str=None)`` - ottieni gli eventi in cui l'utente ha fatto assenza a partire da una certa data

    .. code-block:: python

        async def assenze_da(self, evento: str) -> list[dict[str, Any]]:
    
    Parametri
    
        - ``inizio: str``: data di inizio dell'evento da cui partire, in formato ``YYYY-MM-DD``
    
    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi in cui l'utente ha fatto assenza in formato JSON
    
    Eccezioni
    
        - ``classeviva.eccezioni.FormatoNonValido`` - il formato della data non è valido
        - ``classeviva.eccezioni.DataFuoriGamma`` - la data non appartiene all'anno scolastico corrente
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP


    - ``await self.assenze_da_a(inizio: str=None, fine: str=None)`` - ottieni gli eventi compresi tra due date in cui l'utente ha fatto assenza

    .. code-block:: python

        async def assenze_da_a(self, inizio: str=None, fine: str=None) -> list[dict[str, Any]]:
    
    Parametri

        - ``inizio: str``: data di inizio degli eventi da cui partire, in formato ``YYYY-MM-DD``
        - ``fine: str``: data di fine degli eventi fino a cui partire, in formato ``YYYY-MM-DD``
    
    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi in cui l'utente ha fatto assenza
    
    Eccezioni

        - ``classeviva.eccezioni.FormatoNonValido`` - il formato della data non è valido
        - ``classeviva.eccezioni.DataFuoriGamma`` - la data non appartiene all'anno scolastico corrente, oppure la data di fine è precedente alla data di inizio
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP


    - ``await self.agenda_da_a(inizio: str, fine: str)`` - ottieni gli eventi che compongono l'agenda dell'utente

    .. code-block:: python

        async def agenda_da_a(self, inizio: str=None, fine: str=None) -> list[dict[str, Any]]:

    Parametri

        - ``inizio: str``: data di inizio degli eventi da cui partire, in formato ``YYYY-MM-DD``
        - ``fine: str``: data di fine degli eventi fino a cui restituirli, in formato ``YYYY-MM-DD``
    
    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi dell'argenda nel periodo di tempo specificato
    
    Eccezioni

        - ``classeviva.eccezioni.FormatoNonValido`` - il formato della data non è valido
        - ``classeviva.eccezioni.DataFuoriGamma`` - la data non appartiene all'anno scolastico corrente, oppure la data di fine è precedente alla data di inizio
        - ``classeviva.eccezioni.ErroreHTTP404`` - eccezione generata in caso di errore HTTP 404
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP di altro tipo


    - ``await self.agenda_codice_da_a(codice: str, inizio: str, fine: str)`` - ottieni gli eventi dell'utente con un determinato codice evento

    .. code-block:: python

        async def agenda_codice_da_a(self, codice: str, inizio: str=None, fine: str=None) -> list[dict[str, Any]]:
    
    Parametri

        - ``codice: str``: codice evento sulla base del quale filtrare gli eventi
        - ``inizio: str``: data di inizio degli eventi da cui partire, in formato ``YYYY-MM-DD``
        - ``fine: str``: data di fine degli eventi fino a cui restituirli, in formato ``YYYY-MM-DD``

    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi dell'argenda nel periodo di tempo specificato che hanno il codice evento specificato

    Eccezioni

        - ``classeviva.eccezioni.FormatoNonValido`` - il formato della data non è valido
        - ``classeviva.eccezioni.DataFuoriGamma`` - la data non appartiene all'anno scolastico corrente, oppure la data di fine è precedente alla data di inizio
        - ``classeviva.eccezioni.ErroreHTTP404`` - eccezione generata in caso di errore HTTP 404
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP di altro tipo


    - ``await self.agenda()`` - ottieni gli eventi dell'utente nell'anno scolastico corrente

    .. code-block:: python

        async def agenda(self) -> list[dict[str, Any]]:
    
    Ritorno

        - ``list[dict[str, Any]]`` - gli eventi dell'agenda nell'anno scolastico corrente
    
    Eccezioni

        - ``classeviva.eccezioni.FormatoNonValido`` - il formato della data non è valido
        - ``classeviva.eccezioni.DataFuoriGamma`` - la data non appartiene all'anno scolastico corrente, oppure la data di fine è precedente alla data di inizio
        - ``classeviva.eccezioni.ErroreHTTP404`` - eccezione generata in caso di errore HTTP 404
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione generata in caso di errore HTTP di altro tipo


    - ``await self.didattica()`` - ottieni il materiale in didattica dell'anno scolastico corrente

    .. code-block:: python

        async def didattica(self) -> list[dict[str, Any]]:

    Ritorno

        - ``list[dict[str, Any]]`` - il materiale in didattica dell'anno scolastico corrente [19]_
    
    Eccezioni
    
        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione sollevata in caso di errore HTTP


    - ``await self.didattica_elemento(contenuto: int)`` - ottieni un contenuto dal materiale in didattica

    .. code-block:: python

        async def didattica_elemento(self, contenuto: int) -> Any:
    
    Parametri

        - ``contenuto: int``: codice del contenuto da ottenere

    Ritorno

        - ``Any`` - il contenuto richiesto

        Avvertenze

            - L'endpoint restituisce lo stesso contenuto di ``didattica()``
    
    Eccezioni

        - ``classeviva.eccezioni.ErroreHTTP`` - eccezione sollevata in caso di errore HTTP


Metodi magici [11]_

    - ``self.__call__()`` | ``self()`` - connette in modo sincrono l'utente

    .. code-block:: python

        def __call__(self) -> None:
            asyncio.run(self.accedi())
    
    - ``self.__eq__()`` - gestisce le uguaglianze

    .. code-block:: python

        def __eq__(self, other) -> bool:
            if (isinstance(other, Utente)):
                return (self.id == other.id and self.password == other.password)
            return False


Decoratori

    - ``@classeviva.Utente.connettente`` - passa l'utente alla funzione come primo parametro dopo aver chiamato il metodo ``accedi()``

    .. code-block:: python

        @utente_.connettente
        def foo(x: classeviva.Utente) -> None:
            print(x.dati)
    
    Avvertenze

        - Non funziona con le funzioni asincrone (``async def``) [8]_


``ListaUtenti``
---------------------------

Un'espansione di un ``set`` di ``classeviva.Utente``, con metodi utili a eliminare duplicati e ad eseguire in modo asincrono i metodi iterando sugli utenti.


Classe

    .. code-block:: python

        class ListaUtenti(set[Utente])


Costruttore

    .. code-block:: python

        def __init__(
            self, 
            utenti: Iterable[Utente]
        ) -> None:
    
    Parametri:

    - ``utenti: Iterable[Utente]`` - iterabile contenente [9]_ oggetti di tipo ``classeviva.Utente``


Proprietà

    - ``connessi: set[Utente]`` - elenco degli alunni connessi [10]_ della lista

    .. code-block:: python

        @property
        def connessi(self) -> set[Utente]:
            return {utente for utente in self if (utente.connesso)}

    - ``non_connessi: set[Utente]`` - elenco degli alunni non connessi [10]_ della lista

    .. code-block:: python

        @property
        def non_connessi(self) -> set[Utente]:
            return {utente for utente in self if (not utente.connesso)}


Metodi

    - ``await self.accedi()`` - effettua l'accesso alla sessione [6]_ **per tutti gli utenti**

    .. code-block:: python

        async def accedi(self) -> None:
            await asyncio.gather(*[utente.accedi() for utente in self.non_connessi])
    
    - ``self.aggiungi(utente)`` - aggiunge un utente alla lista

    .. code-block:: python

        def aggiungi(self, utente: Utente) -> bool:
            if (isinstance(utente, Utente) and utente not in self):
                self.add(utente)
                return True
            return False
    
    Parametri
    
        - ``utente: Utente``: l'utente da aggiungere
    
    Ritorno

        - ``bool`` - True se l'utente è stato aggiunto, False altrimenti
    
    Avvertenze

        - Utilizza il metodo ``add()`` della classe ``set`` da cui eredita, potrebbe sollevare delle eccezioni non gestite dal programma


Metodi magici [11]_

    - ``self.__call__()`` | ``self()`` - connette in modo sincrono tutti gli utenti

    .. code-block:: python

        def __call__(self) -> None:
            asyncio.run(self.accedi())
    
    - ``self.__add__()`` - gestisce le addizioni (``+``, ``+=``)

    .. code-block:: python

        def __add__(self, oggetto) -> ListaUtenti:
            if (isinstance(oggetto, Utente)):
                self.aggiungi(oggetto)
            elif (isinstance(oggetto, IterableABC)):
                for oggetto_ in oggetto:
                    self.aggiungi(oggetto_)
            else:
                raise TypeError(f"{oggetto} non è un oggetto valido")
    
    - ``self.__contains__()`` - stabilisce se un utente è presente nella lista

    .. code-block:: python

        def __contains__(self, utente: Utente) -> bool:
            if (isinstance(utente, Utente)):
                for utentino in self:
                    if (utente == utentino):
                        return True
            return False


Decoratori

    - ``@classeviva.ListaUtenti.iterante`` - ripete le operazioni della funzione decorata su tutti i membri della lista quando viene chiamata

    .. code-block:: python

        @lista_utenti.iterante
        def foo(x: classeviva.ListaUtenti) -> None:
            print(x.connessi)


``classeviva.collegamenti`` [13]_
===========================
``classeviva.collegamenti`` è il modulo che contiene gli URL per le richieste all'API di ClasseViva. [14]_


``Collegamenti``
---------------------------
La classe ``classeviva.collegamenti.Collegamenti`` contiene gli URL per le richieste all'API di ClasseViva [15]_

L'intero codice del modulo è riportato qui, perché breve ed esemplificativo di sé stesso.

.. code-block:: python

    class Collegamenti:
        base: str = "https://web.spaggiari.eu/rest"
        accesso: str = f"{base}/v1/auth/login"
        stato: str = f"{base}/v1/auth/status"
        biglietto: str = f"{base}/v1/auth/ticket"
        documenti: str = f"{base}/v1/students/{{}}/documents"
        controllo_documento: str = f"{base}/v1/students/{{}}/documents/check/{{}}"
        leggi_documento: str = f"{base}/v1/students/{{}}/documents/read/{{}}"
        assenze: str = f"{base}/v1/students/{{}}/absences/details"


``classeviva.eccezioni``
===========================
``classeviva.eccezioni`` è il modulo che contiene le eccezioni sollevate da funzioni e metodi contenuti in ``classeviva``


``TokenErrore``
---------------------------
Rappresenta tutti gli errori legati al token di accesso all'API

    .. code-block:: python

        class TokenErrore(Exception):
            ...

Sottoclassi

    - ``classeviva.eccezioni.TokenNonValido`` - il token non è riconosciuto come valido dall'API

    .. code-block:: python

        class TokenNonValido(TokenErrore):
            ...
    
    - ``classeviva.eccezioni.TokenScaduto`` - il token è scaduto

    .. code-block:: python

        class TokenScaduto(TokenErrore):
            ...
    
    - ``classeviva.eccezioni.TokenNonPresente`` - il token non è presente, ovvero non è stato effettuato l'accesso

    .. code-block:: python

        class TokenNonPresente(TokenErrore):
            ...


``UtenteErrore``
---------------------------
Rappresenta tutti gli errori legati all'utente e in particolare alla compilazione dei suoi campi obbligatori

    .. code-block:: python

        class UtenteErrore(Exception):
            """
            Errori legati alle utenze
            """

Sottoclassi

    - ``classeviva.eccezioni.PasswordNonValida`` - la password non combacia, l'API non ha potuto accettarla [16]_

    .. code-block:: python

        class PasswordNonValida(UtenteErrore):
            ...

``NonAccesso``
---------------------------
Rappresenta tutti gli errori probabilmente dovuti ad un mancato accesso, e che non rientrano in un'altra categoria [17]_

.. code-block:: python

    class NonAccesso(Exception):
        """
        Errori dovuti a un mancato accesso
        """

Sottoclassi

    - ``classeviva.eccezioni.SenzaDati`` - l'utente non ha tra i suoi attributi privati quelli dati dall'accesso

    .. code-block:: python

        class SenzaDati(NonAccesso):
            ...


``ErroreHTTP``
---------------------------
Rappresenta tutti gli errori HTTP provenienti dalle richieste fatte col modulo ``requests``

.. code-block:: python

    class ErroreHTTP(Exception):
        ...

Fornisce tutte le informazioni date dalla risposta di ``requests`` [18]_

.. code-block:: python

    raise e.ErroreHTTP(f"""
            Richiesta non corretta, codice {response.status_code}
            {response.text}
            {response.json()}
        """)

Sottoclassi

    - ``classeviva.eccezioni.ErroreHTTP404`` - la richiesta ha restituito un errore 404

    .. code-block:: python

        class ErroreHTTP404(ErroreHTTP):
            ...

``classeviva.variabili``
===========================
``classeviva.variabili`` è il modulo che contiene le costanti utili per evitare ridondanza nel codice

L'intero codice del modulo è riportato qui, perché breve ed esemplificativo di sé stesso.

.. code-block:: python

    # Constante che indica il tempo di connessione per una sessione
    TEMPO_CONNESSIONE: int = 1800


    # Constante che indica l'intestazione per le richieste
    intestazione: dict[str, str] = {
        "content-type": "application/json",
        "Z-Dev-ApiKey": "+zorro+",
        "User-Agent": "zorro/1.0"
    }


Note
===========================

.. [JSON] Per "formato ``JSON``" si intende il formato restituito dall'``API``, che non corrisponde con il valore di ritorno della funzione che, utilizzando il modulo ``json``, converte i dati in oggetti di Python
.. [1] Studente, in Classeviva, è un utente il cui identificatore inizia con il carattere 'S'
.. [2] Biglietto, in Classeviva, è una stringa di caratteri, ma non si è ancora capito a cosa serva
.. [3] `Richiesta di stato <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/status.md>`_
.. [4] Sezione "schoolReport" della risposta alla `richiesta di documenti <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/documents.md>`_
.. [5] Sezione "documents" della risposta alla `richiesta di documenti <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Documents/documents.md>`_
.. [6] `Richiesta di accesso <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/login.md>`_
.. [7] `Richiesta di assenze <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Absences/absences.md>`_
.. [8] Alla versione ``0.1.0``, ma è un miglioramento che verrà aggiunto in futuro
.. [9] Non è necessario che contenga soltanto oggetti di quel tipo, grazie al metodo privato ``__riduci``
.. [10] Vengono verificati tramite la loro proprietà ``Utente.connesso``
.. [11] Sono riportati i metodi magici la cui sovrascrittura è rilevante ai fini dell'utilizzo del modulo, gli altri possno essere trovati nel codice sorgente
.. [12] Il metodo ``__call__`` è un metodo magico, che viene chiamato quando si fa ``utente()``
.. [13] Il modulo, alla versione ``0.1.0``, è comprensivo di un solo namespace contenente URL
.. [14] Il suo utilizzo è volto alla fase di sviluppo, ma può essere adoperato anche in fase di produzione in caso di necessità
.. [15] Per ogni versione sono disponibili soltanto gli URL per le richieste le cui rispettive funzioni sono già implementate
.. [16] L'API lo comunica tramite una risposta ``HTTP`` con codice ``422``
.. [17] Ne è un esempio ``TokenNonPresente``, che pur rientrando nella descrizione di ``NonAccesso`` non ne è sottoclasse perché già parte di ``TokenErrore``
.. [18] Alla versione ``0.1.0`` va fatto manualmente sollevando l'eccezione come descritto sotto
.. [19] La struttura dei dizionari contenuti nella lista è complessa, può essere trovata `qui <https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Didactics/didactics.md>`