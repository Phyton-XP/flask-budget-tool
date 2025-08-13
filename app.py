# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
import os
from utils.functions import (
    # DB/Settings
    get_connection, ensure_settings, get_setting, set_setting,
    # Zyklus/Datum
    get_start_day, get_end_day, get_cycle_for_date, get_current_week,
    get_current_month_range, get_next_monday, is_valid_cycle,
    # Aktivierung/Übertrag
    guarded_wochenuebertrag, get_last_week_balance, is_transfer_active,
    activated_this_week, get_last_transfer_date,
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "change-me-please"

print("ROOT_PATH:", app.root_path)
print("TEMPLATE_SEARCHPATH:", getattr(app.jinja_loader, "searchpath", None))

# einmal beim Start versuchen
try:
    ensure_settings()
except Exception as e:
    print(f"ensure_settings() übersprungen: {e}")

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only")

# --------- Jinja-Filter ----------
@app.template_filter('datetimeformat')
def datetimeformat(value, format="%d.%m.%Y"):
    if value is None:
        return "-"
    if isinstance(value, datetime):
        return value.strftime(format)
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").strftime(format)
    return str(value)

# --------- Context Processor ----------
@app.context_processor
def inject_reset_countdown():
    now = datetime.now()
    next_reset = get_next_monday()
    remaining = next_reset - now
    return dict(
        countdown_days=remaining.days,
        countdown_hours=remaining.seconds // 3600,
        countdown_minutes=(remaining.seconds % 3600) // 60,
    )

# --------- Settings Routes ----------
@app.route("/update-startday", methods=["POST"])
def update_startday():
    try:
        new_day = int(request.form["start_day"])
    except (KeyError, ValueError, TypeError):
        new_day = 27
    new_day = max(1, min(31, new_day))

    end_day = get_end_day()
    if not is_valid_cycle(new_day, end_day):
        flash("Ungültiger Zeitraum: Zwischen Start- und Endtag müssen mindestens 7 Tage liegen.", "error")
        return redirect(url_for("index"))

    set_setting("start_day", new_day)
    flash("Starttag gespeichert.", "success")
    return redirect(url_for("index"))

@app.route("/update-endday", methods=["POST"])
def update_endday():
    try:
        new_day = int(request.form["end_day"])
    except (KeyError, ValueError, TypeError):
        new_day = 26
    new_day = max(1, min(31, new_day))

    start_day = get_start_day()
    if not is_valid_cycle(start_day, new_day):
        flash("Ungültiger Zeitraum: Zwischen Start- und Endtag müssen mindestens 7 Tage liegen.", "error")
        return redirect(url_for("index"))

    set_setting("end_day", new_day)
    flash("Endtag gespeichert.", "success")
    return redirect(url_for("index"))

@app.route("/update-budget", methods=["POST"])
def update_budget():
    raw_input = (request.form.get("monatsbudget", "0") or "").replace(",", ".").strip()
    try:
        monatsbudget = float(raw_input)
    except ValueError:
        monatsbudget = 0.0

    set_setting("monatsbudget", monatsbudget)

    # Aktivierung setzen, falls erstmals > 0
    if monatsbudget > 0 and not get_setting("activated_at", None):
        set_setting("activated_at", datetime.today().strftime("%Y-%m-%d"))

    return redirect(url_for("index"))

# --------- Hauptseite ----------
@app.route("/", methods=["GET", "POST"])
def index():
    guarded_wochenuebertrag()  # macht nichts, wenn (noch) nicht aktiv

    heute = datetime.today()
    week_start, week_end = get_current_week()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT value FROM einstellungen WHERE key = 'monatsbudget'")
    row = cur.fetchone()
    monatsbudget = float(row[0]) if row and row[0] is not None else 0.0

    start_day = get_start_day()
    end_day = get_end_day()
    zyklus_start, zyklus_ende = get_cycle_for_date(heute.date(), start_day, end_day)
    tage_gesamt = (zyklus_ende - zyklus_start).days + 1

    tagesbudget = monatsbudget / tage_gesamt if tage_gesamt > 0 else 0.0
    wochenbudget = round(tagesbudget * 7, 2)

    # Ausgaben dieser Woche
    cur.execute(
        "SELECT SUM(betrag) FROM ausgaben WHERE date(datum) BETWEEN ? AND ?",
        (week_start.isoformat(), week_end.isoformat())
    )
    row = cur.fetchone()
    summe = float(row[0]) if row and row[0] is not None else 0.0
    ausgegeben = abs(summe)

    # POST: neue Ausgabe
    if request.method == "POST":
        raw_amount = (request.form.get("betrag", "") or "").replace(",", ".").strip()
        beschreibung = request.form.get("beschreibung", "").strip()
        try:
            betrag = -abs(float(raw_amount))
        except ValueError:
            conn.close()
            return redirect(url_for("index", err="invalid_amount"))

        datum = datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO ausgaben (datum, betrag, beschreibung) VALUES (?, ?, ?)", (datum, betrag, beschreibung))
        conn.commit()
        return redirect(url_for("index"))

    # Einträge dieser Woche
    cur.execute(
        "SELECT * FROM ausgaben WHERE date(datum) BETWEEN ? AND ? ORDER BY datum DESC",
        (week_start.isoformat(), week_end.isoformat())
    )
    eintraege = cur.fetchall()
    conn.close()

    # Übertrag
    uebertrag = get_last_week_balance() if is_transfer_active(date.today()) else 0.0
    if activated_this_week():
        uebertrag = 0.0
        last_transfer_value = None
    else:
        last_transfer_value = get_last_transfer_date()

    verbleibend = round(wochenbudget + uebertrag - ausgegeben, 2)
    monatsrange = f"{zyklus_start.strftime('%d.%m.')}–{zyklus_ende.strftime('%d.%m.')}"

    return render_template(
        "index.html",
        monatsbudget=monatsbudget,
        monatsrange=monatsrange,
        tagesbudget=round(tagesbudget, 2),
        wochenbudget=round(wochenbudget, 2),
        ausgegeben=round(ausgegeben, 2),
        rest=verbleibend,
        eintraege=eintraege,
        uebertrag=round(uebertrag, 2),
        start_day=start_day,
        end_day=end_day,
        tage_gesamt=tage_gesamt,
        last_transfer=last_transfer_value,
        show_transfer=not activated_this_week(),
    )

# --------- Wartung ----------
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ausgaben WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/clear-expenses", methods=["POST"])
def clear_expenses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ausgaben")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/clear-budgets", methods=["POST"])
def clear_budgets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE einstellungen SET value = 0 WHERE key = 'monatsbudget'")
    cur.execute("DELETE FROM transfer_log")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
