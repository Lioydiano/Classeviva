from datetime import datetime
from typing import Type
import classeviva.eccezioni as e


# Constante che indica il tempo di connessione per una sessione in secondi
TEMPO_CONNESSIONE: int = 5400


# Constante che indica l'intestazione per le richieste
intestazione: dict[str, str] = {
    "content-type": "application/json",
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",
    "User-Agent": "CVVS/std/4.2.3 Android/12",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://web.spaggiari.eu",
    "Referer": "https://web.spaggiari.eu/home/app/default/login.php?target=&mode=",
}


def valida_date(*dates_: str) -> Type[datetime.date] | tuple[Type[datetime.date]]:
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
    try:
        dates = tuple(datetime.strptime(date, "%Y-%m-%d").date() for date in dates_)
    except ValueError:
        raise e.FormatoNonValido("Formato data non valido, dev'essere YYYY-MM-DD")

    if len(dates) == 1:
        return dates[0]

    return dates

def valida_inizio_fine(inizio: str | None, fine: str | None) -> tuple[Type[datetime.date], Type[datetime.date]]:
    return (
        valida_date(inizio) if inizio else data_inizio_anno(),
        valida_date(fine) if fine else data_fine_anno(),
    )

def valida_anno(*year_: str) -> None:
    try:
        for year in year_:
            datetime.strptime(year, r'%y')
    except ValueError:
        raise e.FormatoNonValido("Formato anno non valido, dev'essere YY ('26' per 2026, '27' per 2027, ...)")


def anno() -> int:
    # Return the academic-year start year:
    # if current month >= September, the academic year starts this calendar year,
    # otherwise it started the previous calendar year.
    now = datetime.now()
    return now.year if now.month >= 9 else now.year - 1


def data_inizio_anno() -> str:
    return f"{anno()}0901"


def data_fine_anno() -> str:
    return f"{anno()+1}0630"


def data_fine_anno_o_oggi() -> str:
    # Restituisce la data di fine anno scolastico o quella del giorno corrente
    end_of_school = datetime(anno()+1, 6, 30)
    if datetime.now() <= end_of_school:
        return datetime.now().strftime('%Y%m%d')
    return data_fine_anno()