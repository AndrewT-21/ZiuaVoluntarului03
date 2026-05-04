from flask import Flask, request, render_template
import psycopg2
import os

app = Flask(__name__)

# 🔥 DATABASE (Render / Production)
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        nume_familie = request.form.get('nume_familie')
        prenume = request.form.get('prenume')
        varsta = int(request.form.get('varsta', 0))
        telefon = request.form.get('telefon')
        judet = request.form.get('judet')
        oras = request.form.get('oras')
        email = request.form.get('email')

        if varsta > 18:
            acord_parinti = True
        else:
            acord_parinti = True if request.form.get('acord_parinti') == '1' else False

        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO inscrieri 
                (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nume_familie, prenume, varsta, telefon, judet, oras, email, acord_parinti))

            conn.commit()
            cur.close()

            return "Succes!"

        except Exception as e:
            return f"Eroare: {e}"

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
