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