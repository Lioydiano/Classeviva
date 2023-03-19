Inclusione
===========================
Di seguito è spiegato come ottenere il pacchetto nel proprio script di ``Python``


Scarica
===========================
Il pacchetto può essere scaricato da `PyPI <https://pypi.org>`_ tramite ``pip``, il progetto si trova `qui <https://pypi.org/project/Classeviva.py/>`_

.. code-block:: bash

    python -m pip install Classeviva.py


Importazione
===========================
Una volta installato il pacchetto, i suoi moduli possono essere importati tramite il comando ``import``

.. code-block:: python

    import classeviva # importa il modulo
    import classeviva.eccezioni # importa il modulo che contiene le eccezioni
    from classeviva import * # importa tutto da Classeviva.py

Facendo questo si tenga conto che il modulo ``classeviva`` contiene anche i sottomoduli, grazie a queste importazioni

.. code-block:: python

    from .collegamenti import collegamenti as c
    from .eccezioni import eccezioni as e
    from .variabili import variabili as v

Quindi è possibile includere nel proprio programma i sottomoduli in un altro modo, seppur sconsigliato

.. code-block:: python

    from classeviva import c as collegamenti # importa il sottomodulo collegamenti passando da classeviva


Intro [1]_
===========================
Per iniziare può essere utile visionare i primi passi per l'interazione con l'API di Classeviva

Utente
---------------------------
- Inizializzare una variabile ``utente`` con un oggetto di tipo ``classeviva.Utente``

.. code-block:: python

    >>> from classeviva import *
    >>> utente = classeviva.Utente("S8733880I", "PasswordSegretissima")

- Iniziare la sessione di accesso all'API, che durerà ``5400`` secondi

.. code-block:: python

    >>> utente()

- Verificare se la sessione è attiva

.. code-block:: python

    >>> utente.stato
    True

- Verificare se il tempo è trascorso **senza fare richieste HTTP**

.. code-block:: python

    >>> utente.connesso
    False

- Richiedere l'elenco dei documenti e richiedere la conferma dell'esistenza del documento

.. code-block:: python

    >>> doc = asyncio.run(utente.documenti())
    >>> print(asyncio.run(utente.controlla_documento(doc["documents"][0]["hash"])))
    True

- Richiedere l'elenco delle assenze e assegnarle a una variabile

.. code-block:: python

    >>> assenze = asyncio.run(utente.assenze())

- Richiedere l'elenco delle lezioni di una determinata materia in un range di date

.. code-block:: python

    >>> lezioni = asyncio.run(utente.lezioni_da_a_materia("2023-01-01", "2023-01-31", "206164"))
    [
        ...,
        {
            'evtId': 9673367,
            'evtDate': '2023-01-26',
            'evtCode': 'LSF0',
            'evtHPos': 4,
            'evtDuration': 1,
            'classDesc': '3QS SCIENTIFICO - OPZIONE SCIENZE APPLICATE QUADRIENNALE',
            'authorName': 'Nome Cognome', # Nome e cognome dell'insegnante
            'subjectId': 206164, # ID della materia (in questo caso Informatica), lo stesso ID usato come parametro per lezioni_da_a_materia
            'subjectCode': None,
            'subjectDesc': 'INFORMATICA',
            'lessonType': 'Attività di laboratorio',
            'lessonArg': 'Correzione esercizio per casa. Creazione di progetti con classi in file separati.'
        },
        {
            'evtId': 9881475,
            'evtDate': '2023-01-28',
            'evtCode': 'LSF0',
            'evtHPos': 4,
            'evtDuration': 1,
            'classDesc': '3QS SCIENTIFICO - OPZIONE SCIENZE APPLICATE QUADRIENNALE',
            'authorName': 'ANTONIAZZI ALESSANDRA',
            'subjectId': 206164,
            'subjectCode': None,
            'subjectDesc': 'INFORMATICA',
            'lessonType': 'Attività di laboratorio',
            'lessonArg': 'Lavoro di gruppo: creazione videogioco OOP in C++'
        },
        ...
    ]

Note
===========================
.. [1] In tutto il tutorial d'introduzione sono utilizzate delle credenziali fittizie, ovvero ``S8733880I`` e ``PasswordSegretissima``. Per fare dei tentativi occorre utilizzare delle credenziali esistenti.