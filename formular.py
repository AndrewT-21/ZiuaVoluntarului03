from flask import Flask, request, render_template, Response
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_conn():
    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        varsta = int(request.form.get('varsta', 0))
        telefon = request.form.get('telefon')
        judet = request.form.get('judet')
        oras = request.form.get('oras')
        email = request.form.get('email')

        if varsta < 18:
            acord = True if request.form.get('acord-parinti') == '1' else False
        else:
            acord = True

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO inscrieri
            (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (nume, prenume, varsta, telefon, judet, oras, email, acord))

        conn.commit()
        cur.close()
        conn.close()

        return "success"

    return render_template('index.html')


@app.route('/vizualizare')
def vizualizare():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inscrieri ORDER BY id DESC")
    inscrieri = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('vizualizare.html', inscrieri=inscrieri)


@app.route('/export')
def export():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM inscrieri")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    def generate():
        for row in rows:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(),
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=inscrieri.csv"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
