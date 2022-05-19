class Collegamenti:
    base: str = "https://web.spaggiari.eu/rest"
    accesso: str = f"{base}/v1/auth/login"
    stato: str = f"{base}/v1/auth/status"
    biglietto: str = f"{base}/v1/auth/ticket"
    documenti: str = f"{base}/v1/students/{{}}/documents"