class TokenErrore(Exception):
    ...


class TokenNonValido(TokenErrore):
    ...


class TokenScaduto(TokenErrore):
    ...


class UtenteErrore(Exception):
    """
    Errori legati alle utenze
    """


class PasswordNonValida(UtenteErrore):
    """
    Password non valida
    """