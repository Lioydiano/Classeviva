Inclusione
===========================
Di seguito è spiegato come ottenere il pacchetto nel proprio script di ``Python``


Scarica
===========================
Il pacchetto può essere scaricato da `PyPI <https://pypi.org>` tramite ``pip``, il progetto si trova `qui <https://pypi.org/project/Classeviva.py/>`

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


Note
===========================
.. [1] In tutto il tutorial d'introduzione sono utilizzate delle credenziali fittizie, ovvero ``S8733880I`` e ``PasswordSegretissima``. Per fare dei tentativi occorre utilizzare delle credenziali esistenti.