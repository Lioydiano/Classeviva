from requests import Response


class TokenErrore(Exception):
    ...


class TokenNonValido(TokenErrore):
    ...


class TokenScaduto(TokenErrore):
    ...


class TokenNonPresente(TokenErrore):
    ...


class UtenteErrore(Exception):
    """
    Errori legati alle utenze
    """


class PasswordNonValida(UtenteErrore):
    ...


class NonAccesso(Exception):
    """
    Errori dovuti a un mancato accesso
    """


class SenzaDati(NonAccesso):
    ...


class ErroreHTTP(Exception):
    ...


class ErroreHTTP404(ErroreHTTP):
    ...


class DataErrore(Exception):
    """
    Errori legati alle date
    """


class FormatoNonValido(DataErrore):
    """
    Formato della data non valido (il formato del parametro deve essere YYYY-MM-DD)
    """


class DataFuoriGamma(DataErrore):
    """
    Data al di fuori della gamma di date valide per l'anno scolastico
    
    "dates must be beween 20210901 and 20220531; first date be NOT greater than second one"
    (Le date devono essere tra il primo di Settembre e il giorno corrente O la fine dell'anno scolastico)
    """


class ValoreNonValido(Exception):
    """
    Errori legati ai valori
    """


class ParametroNonValido(ValoreNonValido):
    """
    Errori legati ai parametri
    Sollevati quando l'URI esiste ma i parametri forniti causano un errore
    """


class CategoriaNonPresente(ValoreNonValido):
    """
    Errori legati alle categorie
    Sollevati quando l'URI non esiste perché un sotto-endpoint non viene trovato
    """


def sollevaErroreHTTP(response: Response) -> None:
    if isinstance(response, Response):
        try:
            if (response.status_code == 404):
                raise ErroreHTTP404(f"""
                    Testo: {response.text}
                    Risposta: {response.json()}
                """)
            raise ErroreHTTP(f"""
                    Richiesta non corretta 
                    Codice: {response.status_code}
                    Testo: {response.text}
                    Risposta: {response.json()}
                """)
        except AttributeError:
            raise ErroreHTTP("Richiesta non corretta")