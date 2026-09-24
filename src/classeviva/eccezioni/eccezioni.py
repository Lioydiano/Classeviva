from requests import Response


class TokenErrore(Exception):
    pass


class TokenNonValido(TokenErrore):
    pass


class TokenScaduto(TokenErrore):
    pass


class TokenNonPresente(TokenErrore):
    pass


class UtenteErrore(Exception):
    """
    Errori legati alle utenze
    """
    pass


class PasswordNonValida(UtenteErrore):
    pass


class NonAccesso(Exception):
    """
    Errori dovuti a un mancato accesso
    """
    pass


class SenzaDati(NonAccesso):
    pass


class ErroreHTTP(Exception):
    pass


class ErroreHTTP404(ErroreHTTP):
    pass


class DataErrore(Exception):
    """
    Errori legati alle date
    """
    pass


class FormatoNonValido(DataErrore):
    """
    Formato della data non valido (il formato del parametro deve essere YYYY-MM-DD)
    """
    pass


class DataFuoriGamma(DataErrore):
    """
    Data al di fuori della gamma di date valide per l'anno scolastico
    
    "dates must be between Sep 01 (this school-year's) and May 31 (this school year's); first date be NOT greater than second one"
    (Le date devono essere tra il primo di Settembre e il giorno corrente/la fine dell'anno scolastico)
    """
    pass


class ValoreNonValido(Exception):
    """
    Errori legati ai valori
    """
    pass


class ParametroNonValido(ValoreNonValido):
    """
    Errori legati ai parametri
    Sollevati quando l' URI esiste ma i parametri forniti causano un errore
    """
    pass


class CategoriaNonPresente(ValoreNonValido):
    """
    Errori legati alle categorie
    Sollevati quando l' URI non esiste perché un sotto-endpoint non viene trovato
    """
    pass


def ottieniErroreHTTP(response: Response) -> Exception:
    if isinstance(response, Response):
        try:
            if response.status_code == 404:
                return ErroreHTTP404(f"""
                    Testo: {response.text}
                    Risposta: {response.json()}
                """)
            return ErroreHTTP(f"""
                    Richiesta non corretta 
                    Codice: {response.status_code}
                    Testo: {response.text}
                    Risposta: {response.json()}
                """)
        except AttributeError:
            return ErroreHTTP("Richiesta non corretta")
    raise TypeError(f"Il parametro \'response\' di classeviva.eccezioni.sollevaErroreHTTP deve essere di tipo requests.Response, non \'{type(response).__name__}\'")