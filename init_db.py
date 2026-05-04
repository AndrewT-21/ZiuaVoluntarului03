import sqlite3

conn = sqlite3.connect('baza_de_date.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS inscriere (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume_familie TEXT NOT NULL,
        prenume TEXT NOT NULL,
        varsta INTEGER NOT NULL,
        telefon TEXT NOT NULL,
        judet TEXT NOT NULL,
        oras TEXT NOT NULL,
        email TEXT NOT NULL,
        acord_parinti INTEGER
    )
''')

conn.commit()
conn.close()
