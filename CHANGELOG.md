# Changelog

## [1.3.0] - Ottobre 2026

### Added

- `Utente.chi_sono()`, `compiti()`, `media()` e `comunicazioni_ministero()`.
- Timeout di 15 secondi di default
- Un numero `allegato` opzionale per scaricare dalla bacheca specifici file

### Changed

- Aggiornati gli URL di alcuni endpoint
- Le richieste con un intervallo di date inviano le date nel formato richiesto dall'API.
- `ListaUtenti + utente` ora genera una nuova lista; `ListaUtenti += utente` modifica ancora quella originale. **Il comportamento di `+` non corrisponde a quello della v1.2.11**, ma accettiamo questo cambiamento in qualità di bug fix

### Fixed

- Corretto il parsing dell'ID utente
- Corretta la gestione dei reindirizzamenti durante l'accesso
- Gestite le risposte di errore HTTP non in formato JSON

[1.3.0]: https://github.com/Lioydiano/Classeviva/compare/v1.2.11...v1.3.0
