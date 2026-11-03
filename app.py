"""CarCare Tracker - Sprint 1.

A small Flask app that lets a user save vehicles (make, model, year,
mileage), view them in a list, and update a vehicle's mileage.
Data is stored in a local SQLite file (data/carcare.db) so it survives
page refreshes and application restarts.
"""
import os
import sqlite3
from datetime import datetime

from flask import Flask, flash, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("CARCARE_DB", os.path.join(BASE_DIR, "data", "carcare.db"))

app = Flask(__name__)
# Placeholder key, fine for local development. Override with SECRET_KEY in .env/environment.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

MAX_MILEAGE = 2_000_000


def get_db():
    if "db" not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER,
            mileage INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    db.commit()


def parse_mileage(raw):
    """Return (value, error). Mileage must be a whole number 0..MAX_MILEAGE."""
    raw = (raw or "").strip().replace(",", "")
    if not raw:
        return None, "Mileage is required."
    if not raw.isdigit():
        return None, "Mileage must be a whole number (0 or greater)."
    value = int(raw)
    if value > MAX_MILEAGE:
        return None, f"Mileage must be {MAX_MILEAGE:,} or less."
    return value, None


@app.route("/")
def index():
    init_db()
    vehicles = get_db().execute(
        "SELECT * FROM vehicles ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", vehicles=vehicles)


@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    init_db()
    make = request.form.get("make", "").strip()
    model = request.form.get("model", "").strip()
    year_raw = request.form.get("year", "").strip()
    errors = []

    if not make:
        errors.append("Make is required.")
    if not model:
        errors.append("Model is required.")

    year = None
    if year_raw:
        current_year = datetime.now().year
        if not year_raw.isdigit() or not (1900 <= int(year_raw) <= current_year + 1):
            errors.append(f"Year must be a number between 1900 and {current_year + 1}.")
        else:
            year = int(year_raw)

    mileage, mileage_error = parse_mileage(request.form.get("mileage"))
    if mileage_error:
        errors.append(mileage_error)

    if errors:
        for message in errors:
            flash(message, "error")
        return redirect(url_for("index"))

    db = get_db()
    db.execute(
        "INSERT INTO vehicles (make, model, year, mileage, updated_at) VALUES (?, ?, ?, ?, ?)",
        (make, model, year, mileage, datetime.now().strftime("%Y-%m-%d %H:%M")),
    )
    db.commit()
    flash(f"Added {make} {model}.", "success")
    return redirect(url_for("index"))


@app.route("/vehicles/<int:vehicle_id>/mileage", methods=["POST"])
def update_mileage(vehicle_id):
    init_db()
    db = get_db()
    vehicle = db.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
    if vehicle is None:
        flash("Vehicle not found.", "error")
        return redirect(url_for("index"))

    mileage, error = parse_mileage(request.form.get("mileage"))
    if error:
        flash(error, "error")
    elif mileage < vehicle["mileage"]:
        flash(
            f"New mileage ({mileage:,}) cannot be lower than the current "
            f"mileage ({vehicle['mileage']:,}).",
            "error",
        )
    else:
        db.execute(
            "UPDATE vehicles SET mileage = ?, updated_at = ? WHERE id = ?",
            (mileage, datetime.now().strftime("%Y-%m-%d %H:%M"), vehicle_id),
        )
        db.commit()
        flash(f"Updated {vehicle['make']} {vehicle['model']} to {mileage:,} miles.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
