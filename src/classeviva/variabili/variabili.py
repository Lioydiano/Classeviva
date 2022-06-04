# Constante che indica il tempo di connessione per una sessione in secondi
TEMPO_CONNESSIONE: int = 5400


# Constante che indica l'intestazione per le richieste
intestazione: dict[str, str] = {
    "content-type": "application/json",
    "Z-Dev-ApiKey": "+zorro+",
    "User-Agent": "zorro/1.0"
}