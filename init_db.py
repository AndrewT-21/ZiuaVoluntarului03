import os
from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

# 🔥 ia URL-ul din Render Environment Variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# 🔥 conexiune PostgreSQL cu SSL corect (OBLIGATORIU pe Render)
conn = psycopg2.connect(
    DATABASE_URL,
    sslmode="require"
)

cur = conn.cursor()

# 🔥 creare tabel (dacă nu există)
cur.execute("""
CREATE TABLE IF NOT EXISTS inscriere (
    id SERIAL PRIMARY KEY,
    nume_familie TEXT NOT NULL,
    prenume TEXT NOT NULL,
    varsta INTEGER NOT NULL,
    telefon TEXT NOT NULL,
    judet TEXT NOT NULL,
    oras TEXT NOT NULL,
    email TEXT NOT NULL,
    acord_parinti INTEGER
)
""")

conn.commit()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        varsta = request.form["varsta"]
        telefon = request.form["telefon"]
        judet = request.form["judet"]
        oras = request.form["oras"]
        email = request.form["email"]
        acord = request.form.get("acord-parinti", 0)

        cur.execute("""
            INSERT INTO inscriere 
            (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nume, prenume, varsta, telefon, judet, oras, email, acord))

        conn.commit()

        return render_template("success.html")

    return render_template("formular.html")


@app.route("/inscrieri")
def inscrieri():
    cur.execute("SELECT * FROM inscriere ORDER BY id DESC")
    data = cur.fetchall()
    return str(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
