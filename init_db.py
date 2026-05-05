import psycopg2

conn = psycopg2.connect(
    host="dpg-d7siafgk1i2s739prs6g-a.oregon-postgres.render.com",
    database="formular",
    user="formular_user",
    password="EboB58d2pBGMVhqXfProSvUDXHfBj08A",
    port=5432
)
cur = conn.cursor()

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
conn.close()
