# Changelog – Flask Budget Tool

Alle nennenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.  
Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/) und [Semantic Versioning](https://semver.org/).

All notable changes to this project will be documented in this file.  
The format is based on [Keep a Changelog](https://keepachangelog.com/) and [Semantic Versioning](https://semver.org/).

---

## [0.9.0] – 2025-08-13
### Added
- [DE] **Monatsbudget-Logik** mit frei wählbarem Start- und Endtag  
- [EN] **Monthly budget logic** with freely selectable start and end date  

- [DE] Wochenreset (montags) mit Vorwochen-Übertrag  
- [EN] Weekly reset (Mondays) with previous week carryover  

- [DE] Weboberfläche mit Bootstrap-Design  
- [EN] Web interface with Bootstrap design  

- [DE] Auslagerung von Hilfsfunktionen in `utils/functions.py`  
- [EN] Helper functions moved to `utils/functions.py`  

- [DE] `requirements.txt` für einfaches Setup  
- [EN] `requirements.txt` for easy setup  

- [DE] Erste README.md mit Quickstart-Anleitung  
- [EN] Initial README.md with quickstart guide  

- [DE] MIT-Lizenz hinzugefügt  
- [EN] Added MIT license  

### Changed
- [DE] Struktur des Codes in `app.py`, `init_db.py` und `utils/` verbessert  
- [EN] Improved code structure in `app.py`, `init_db.py`, and `utils/`  

- [DE] Vorbereitung für GitHub-Release (bereinigter Projektordner)  
- [EN] Prepared for GitHub release (cleaned project folder)  

### Fixed
- [DE] Bug bei Wochenstartberechnung behoben  
- [EN] Fixed bug in weekly start calculation  

- [DE] Fehlerhafte Anzeige bei Übertrag von Restbudget gefixt  
- [EN] Fixed incorrect display of carryover budget  