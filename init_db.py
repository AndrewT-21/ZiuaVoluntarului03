import psycopg2

conn = psycopg2.connect(
    host="dpg-d7sjr3f7f7vs73d4dcog-a.oregon-postgres.render.com",
    database="formular_qzzi",
    user="formular_user",
    password="AFvqFyk7AEi7IuTBrYB35rHguAXu7A4w",
    port=5432
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS formular (
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
conn.close()
