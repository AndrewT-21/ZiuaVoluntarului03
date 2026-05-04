from flask import Flask, request, render_template, redirect, Response
import psycopg2
import csv

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="andrew"
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nume_familie = request.form.get('nume')
        prenume = request.form.get('prenume')
        varsta = int(request.form.get('varsta', 0))
        telefon = request.form.get('telefon')
        judet = request.form.get('judet')
        oras = request.form.get('oras')
        email = request.form.get('email')

        if varsta >= 18:
            acord_parinti = True
        else:
            acord_parinti = True if request.form.get('acord-parinti') == '1' else False

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO inscrieri 
                (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti))

            conn.commit()
            cur.close()

            return "success"

        except Exception as e:
            return f"Eroare: {e}"

    return render_template('index.html')


# 🔐 Protectie simpla
def check_auth(username, password):
    return username == "admin" and password == "1234"

def authenticate():
    return Response(
        'Acces interzis!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.route('/vizualizare')
def vizualizare():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    cur = conn.cursor()
    cur.execute("SELECT * FROM inscrieri ORDER BY created_at DESC")
    inscrieri = cur.fetchall()
    cur.close()

    return render_template('vizualizare.html', inscrieri=inscrieri)


@app.route('/export')
def export():
    cur = conn.cursor()
    cur.execute("SELECT * FROM inscrieri")
    rows = cur.fetchall()
    cur.close()

    def generate():
        for row in rows:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(),
                    mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=inscrieri.csv"})


if __name__ == '__main__':
    app.run(debug=True)