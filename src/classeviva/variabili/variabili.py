from datetime import datetime
import classeviva.eccezioni as e


# Constante che indica il tempo di connessione per una sessione in secondi
TEMPO_CONNESSIONE: int = 5400


# Constante che indica l'intestazione per le richieste
intestazione: dict[str, str] = {
    "content-type": "application/json",
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",
    "User-Agent": "CVVS/std/4.2.3 Android/12"
}


def valida_date(*date_: str) -> None:
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    try:
        for data in date_:
            datetime.strptime(data, r'%Y-%m-%d')
    except ValueError:
        raise e.FormatoNonValido("Formato data non valido, dev'essere YYYY-MM-DD")


def anno() -> int:
    return datetime.now().year


def data_inizio_anno() -> str:
    return f"{anno()}0901"


def data_fine_anno() -> str:
    return f"{anno()+1}0630"


def data_fine_anno_o_oggi() -> str:
    # Restituisce la data di fine anno scolastico o quella del giorno corrente
    if (datetime.now() < datetime(anno(), 6, 30)):
        return f"{anno()}{datetime.now().strftime('%m%d')}"
    return data_fine_anno()