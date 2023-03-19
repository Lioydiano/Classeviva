class Collegamenti:
    base: str = "https://web.spaggiari.eu/rest"
    accesso: str = f"{base}/v1/auth/login"
    stato: str = f"{base}/v1/auth/status"
    biglietto: str = f"{base}/v1/auth/ticket"
    documenti: str = f"{base}/v1/students/{{}}/documents"
    controllo_documento: str = f"{base}/v1/students/{{}}/documents/check/{{}}"
    leggi_documento: str = f"{base}/v1/students/{{}}/documents/read/{{}}"
    assenze: str = f"{base}/v1/students/{{}}/absences/details"
    assenze_da: str = f"{base}/v1/students/{{}}/absences/details/{{}}"
    assenze_da_a: str = f"{base}/v1/students/{{}}/absences/details/{{}}/{{}}"
    agenda_da_a: str = f"{base}/v1/students/{{}}/agenda/all/{{}}/{{}}"
    agenda_codice_da_a: str = f"{base}/v1/students/{{}}/agenda/{{}}/{{}}/{{}}"
    didattica: str = f"{base}/v1/students/{{}}/didactics"
    didattica_elemento: str = f"{base}/v1/students/{{}}/didactics/item/{{}}"
    bacheca: str = f"{base}/v1/students/{{}}/noticeboard"
    bacheca_leggi: str = f"{base}/v1/students/{{}}/noticeboard/read/{{}}/{{}}/101"
    bacheca_allega: str = f"{base}/v1/students/{{}}/noticeboard/attach/{{}}/{{}}/101"
    lezioni: str = f"{base}/v1/students/{{}}/lessons/today"
    lezioni_giorno: str = f"{base}/v1/students/{{}}/lessons/{{}}"
    lezioni_da_a: str = f"{base}/v1/students/{{}}/lessons/{{}}/{{}}"
    lezioni_da_a_materia: str = f"{base}/v1/students/{{}}/lessons/{{}}/{{}}/{{}}"
    calendario: str = f"{base}/v1/students/{{}}/calendar/all"
    calendario_da_a: str = f"{base}/v1/students/{{}}/calendar/{{}}/{{}}"
    libri: str = f"{base}/v1/students/{{}}/schoolbooks"
    carta: str = f"{base}/v1/students/{{}}/card"
    voti: str = f"{base}/v1/students/{{}}/grades"
    periodi: str = f"{base}/v1/students/{{}}/periods"
    materie: str = f"{base}/v1/students/{{}}/subjects"
    note: str = f"{base}/v1/students/{{}}/notes/all"
    leggi_nota: str = f"{base}/v1/students/{{}}/notes/{{}}/read/{{}}"
    avatar: str = f"{base}/v1/users/{{}}/avatar"