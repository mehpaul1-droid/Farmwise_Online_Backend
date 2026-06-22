from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

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

class User(BaseModel):
    phone: str
    password: str

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

        return {
            "status": "ok",
            "message": "ثبت‌نام با موفقیت انجام شد"
        }

    except sqlite3.IntegrityError:
        return {
            "status": "error",
            "message": "این شماره قبلاً ثبت شده است"
        }

    finally:
        conn.close()

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
        return {
            "status": "ok",
            "role": result[3]
        }

    return {
        "status": "error",
        "message": "شماره یا رمز اشتباه است"
    }
