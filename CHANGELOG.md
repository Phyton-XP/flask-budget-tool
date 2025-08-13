# Changelog – Flask Budget Tool

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.  
Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/) und [Semantic Versioning](https://semver.org/).

---

## [0.9.0] – 2025-08-13
### Added
- **Monatsbudget-Logik** mit frei wählbarem Start- und Endtag
- Wochenreset (montags) mit Vorwochen-Übertrag
- Weboberfläche mit Bootstrap-Design
- Auslagerung von Hilfsfunktionen in `utils/functions.py`
- `requirements.txt` für einfaches Setup
- Erste README.md mit Quickstart-Anleitung
- MIT-Lizenz hinzugefügt

### Changed
- Struktur des Codes in `app.py`, `init_db.py` und `utils/` verbessert
- Vorbereitung für GitHub-Release (bereinigter Projektordner)

### Fixed
- Bug bei Wochenstartberechnung behoben
- Fehlerhafte Anzeige bei Übertrag von Restbudget gefixt
