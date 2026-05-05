import os
from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


# 🔥 NU mai conectezi aici global
def get_conn():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_conn()
    cur = conn.cursor()

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
        conn.close()

        return render_template("success.html")

    conn.close()
    return render_template("formular.html")


@app.route("/inscrieri")
def inscrieri():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inscriere ORDER BY id DESC")
    data = cur.fetchall()

    conn.close()

    return str(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
