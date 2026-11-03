# CarCare Tracker

A web app for keeping track of your vehicles and their mileage, built as a semester project. The long-term goal is full car maintenance tracking (service history and reminders); Sprint 1 covers the foundation: saving vehicles and keeping their mileage up to date.

**Author:** YOUR NAME HERE
**Sprint:** 1 (first working version)

## Technologies

- Python 3 with [Flask](https://flask.palletsprojects.com/) (web framework)
- SQLite (built into Python, no separate database install needed)
- Plain HTML and CSS (Jinja2 templates)

## Prerequisites

- Python 3.10 or newer (check with `python --version` or `python3 --version`)
- pip (included with Python)
- Git (only needed to clone the repository)

## Installation

Run these commands in the project's root folder (the folder containing `app.py`).

macOS / Linux:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

No configuration is required. Two optional environment variables exist (see `.env.example`):

| Variable | Purpose | Default |
|----------|---------|---------|
| `SECRET_KEY` | Signs the session cookie used for on-screen messages | a development placeholder |
| `CARCARE_DB` | Path of the SQLite database file | `data/carcare.db` |

The app does not read `.env` files. To set a variable, export it in your terminal before running, for example `export SECRET_KEY=anything` (macOS/Linux) or `$env:SECRET_KEY="anything"` (PowerShell).

## Running the application

From the project root, with the virtual environment active:

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in a browser. You should see the "CarCare Tracker" page with an "Add a vehicle" form and an empty "Your vehicles" section. Stop the server with `Ctrl+C`.

The database file `data/carcare.db` is created automatically on first run.

## Trying the Sprint 1 functionality

1. **Add a vehicle:** enter Make `Toyota`, Model `Corolla`, Year `2018`, Mileage `64500` and select **Add Vehicle**. A green confirmation appears and the vehicle shows in the list with `64,500 mi`.
2. **See validation:** select **Add Vehicle** with the form empty. Red messages say Make, Model and Mileage are required, and nothing is added. Also try mileage `abc` or a year of `1800`.
3. **Update mileage:** in the vehicle's row, enter `65200` and select **Update**. The mileage changes to `65,200 mi`.
4. **Mileage cannot go backwards:** enter `60000` in the same row. An error explains the new mileage cannot be lower than the current one.
5. **Persistence:** refresh the page, or stop and restart the server. The vehicle and its latest mileage are still there.

Sample data is fictional; use any values you like.

## Where data is stored

Vehicles are saved in a local SQLite database file (`data/carcare.db`). It survives page refreshes and application restarts. The file is excluded from Git, so each person who runs the app starts with an empty list.

## Known limitations

- No login: anyone who can open the page sees the same vehicles.
- Vehicles cannot yet be edited or deleted; only mileage can be updated.
- Mileage history is not kept (only the latest value and the time it was updated).
- Maintenance records and reminders are planned for later sprints.
- Intended for local use only; it runs Flask's development server and is not deployed.
