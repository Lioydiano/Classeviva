# Intro
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


* ``Utente``
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

        - ``biglietto_completo: dict[str, str]`` - `Biglietto https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/ticket.md`_ [2]_
        - ``biglietto: str`` -  il biglietto, in forma di stringa e non in formato JSON
        - ``secondi_rimasti: int`` - secondi rimasti alla sessione [3]_
        - ``stato: bool`` - comunica se la sessione è ancora attiva
        - ``connesso: bool`` - comunica se la sessione è attiva **senza fare richieste all'API**

    Complesse

        - ``dati: dict[str, str]`` - dati dell'utente

        .. code-block:: python

            return {
                "id": self._dati["ident"],
                "nome": self._dati["firstName"],
                "cognome": self._dati["lastName"]
            }

        - ``pagelle: list[dict[str, str]]`` - pagelle in formato JSON

Note
===========================

.. [1] Studente, in Classeviva, è un utente il cui identificatore inizia con il carattere 'S'
.. [2] Biglietto, in Classeviva, è una stringa di caratteri, ma non si è ancora capito a cosa serva
.. [3] `Richiesta di stato https://github.com/Lioydiano/Classeviva-Official-Endpoints/blob/master/Authentication/status.md`_