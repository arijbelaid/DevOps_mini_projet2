from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import psycopg2
import os
import time

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ChangeMe-123")

def get_db():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

@app.on_event("startup")
def startup():
    for _ in range(10):
        try:
            conn = get_db()
            cur = conn.cursor()
            # On crée la table "contacts" avec les nouveaux champs
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    age INTEGER,
                    email TEXT NOT NULL
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Base de données initialisée (Table contacts).")
            break
        except Exception as e:
            print(f"Attente de la base de données... {e}")
            time.sleep(3)

class Contact(BaseModel):
    nom: str
    prenom: str
    age: int
    email: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        conn = get_db()
        conn.close()
        return {"status": "ready"}
    except:
        raise HTTPException(status_code=503, detail="DB non disponible")

# --- CRUD CONTACTS ---

@app.get("/contacts")
def get_contacts():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, age, email FROM contacts ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "nom": r[1], "prenom": r[2], "age": r[3], "email": r[4]} for r in rows]

@app.post("/contacts")
def create_contact(contact: Contact):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (nom, prenom, age, email) VALUES (%s, %s, %s, %s) RETURNING id", 
                (contact.nom, contact.prenom, contact.age, contact.email))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, **contact.dict()}

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET nom = %s, prenom = %s, age = %s, email = %s WHERE id = %s", 
                (contact.nom, contact.prenom, contact.age, contact.email, contact_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"id": contact_id, **contact.dict()}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Contact supprimé"}