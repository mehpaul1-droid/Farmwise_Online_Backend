from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- MODEL ----------------
class User(BaseModel):
    phone: str
    password: str

# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: User):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (phone, password, role) VALUES (?, ?, ?)",
            (user.phone, user.password, "worker")
        )
        conn.commit()
        return {"status": "ok", "message": "registered"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE phone=? AND password=?",
        (user.phone, user.password)
    )

    result = c.fetchone()
    conn.close()

    if result:
        return {"status": "ok", "role": result[3]}
    return {"status": "fail"}
