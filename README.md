# Flask Budget Tool

Ein leichtgewichtiges Wochenbudget-Tool mit frei wählbarem Monatszyklus (Start-/Endtag), automatischem Wochen-Reset (montags) und Vorwochen-Übertrag.  
Entwickelt & getestet auf Raspberry Pi (Debian-basiertes OS, z. B. Raspberry Pi OS).  
Funktioniert auch auf anderen Linux-Systemen, wenn Python 3 und Flask installiert sind.  

⚠️ **Hinweis:** Offizieller Support nur für Debian-basierte Systeme.  
Unter Windows oder macOS ist eine manuelle Anpassung der Pfade/Installation nötig.

---

## Features
- Frei wählbarer Monatsstart/-endtag
- Automatischer Wochenreset (montags)
- Übertrag von Restbudgets in die neue Woche
- Minimaler Ressourcenverbrauch – perfekt für Raspberry Pi

---

## Installation (Raspberry Pi / Debian)
```bash
# System aktualisieren & Python-Umgebung bereitstellen
sudo apt update && sudo apt install python3 python3-venv python3-pip -y

# Repository klonen
git clone https://github.com/Pyhton-XP/flask-budget-tool.git
cd flask-budget-tool

# Virtuelle Umgebung erstellen & aktivieren
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank initialisieren
python3 init_db.py

# Anwendung starten
python3 app.py
