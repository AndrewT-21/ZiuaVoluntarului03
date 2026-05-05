import os
import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


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
        cur.execute("""
            INSERT INTO inscriere
            (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["nume"],
            request.form["prenume"],
            request.form["varsta"],
            request.form["telefon"],
            request.form["judet"],
            request.form["oras"],
            request.form["email"],
            request.form.get("acord-parinti", 0)
        ))

        conn.commit()
        conn.close()

        return render_template("success.html")

    conn.close()
    return render_template("formular.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
