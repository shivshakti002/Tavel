import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "travelly.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "replace-with-a-secure-key"  # change in production

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_conn()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
    else:
        # ensure tables exist
        conn = get_conn()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

init_db()

# ---------- Pages ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/goa")
def goa():
    return render_template("goa.html")

@app.route("/jaipur")
def jaipur():
    return render_template("jaipur.html")

@app.route("/ladakh")
def ladakh():
    return render_template("ladakh.html")

@app.route("/booking")
def booking():
    return render_template("booking.html")

# ---------- API endpoints ----------
@app.route("/api/book", methods=["POST"])
def api_book():
    form = request.form
    name = form.get("name","").strip()
    email = form.get("email","").strip()
    phone = form.get("phone","").strip()
    travel_date = form.get("date","").strip()
    persons = form.get("persons","").strip()
    package = form.get("package","").strip()
    message = form.get("message","").strip()

    if not name or not email or not phone:
        flash("Name, email and phone are required.", "warning")
        return redirect(url_for("booking"))

    try:
        persons_val = int(persons) if persons else None
    except:
        persons_val = None

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO bookings (name, email, phone, travel_date, persons, package, message)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, travel_date or None, persons_val, package or None, message or None))
    conn.commit()
    conn.close()

    flash("Booking received. Thank you!", "success")
    return redirect(url_for("booking"))

@app.route("/api/contact", methods=["POST"])
def api_contact():
    form = request.form
    name = form.get("name","").strip()
    email = form.get("email","").strip()
    message = form.get("message","").strip()

    if not message:
        flash("Please enter a message.", "warning")
        return redirect(url_for("index"))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name or None, email or None, message))
    conn.commit()
    conn.close()

    flash("Message received. We will contact you shortly.", "success")
    return redirect(url_for("index"))

# ---------- Admin simple views (no auth) ----------
@app.route("/admin/bookings")
def admin_bookings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("admin_bookings.html", bookings=rows)

@app.route("/admin/contacts")
def admin_contacts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return render_template("admin_contacts.html", contacts=rows)

# ---------- Static files serving fallback (if needed) ----------
@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory(os.path.join(BASE_DIR, "static", "images"), filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
