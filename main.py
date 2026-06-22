from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---------------- DB ----------------
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

    c.execute("""
        CREATE TABLE IF NOT EXISTS livestock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_id TEXT,
            name TEXT,
            type TEXT,
            weight REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            income REAL,
            cost REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- MODELS ----------------
class User(BaseModel):
    phone: str
    password: str

class Livestock(BaseModel):
    farm_id: str
    name: str
    type: str
    weight: float

class Farm(BaseModel):
    name: str
    income: float
    cost: float

# ---------------- AUTH ----------------
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
        return {"status": "ok", "message": "ثبت‌نام موفق"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "این شماره قبلاً ثبت شده است"}
    finally:
        conn.close()

@app.post("/login")
def login(user: User):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE phone=? AND password=?",
              (user.phone, user.password))

    result = c.fetchone()
    conn.close()

    if result:
        return {"status": "ok"}
    return {"status": "error", "message": "ورود ناموفق"}

# ---------------- LIVESTOCK ----------------
@app.post("/add-livestock")
def add_livestock(item: Livestock):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO livestock (farm_id, name, type, weight)
        VALUES (?, ?, ?, ?)
    """, (item.farm_id, item.name, item.type, item.weight))

    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.get("/livestock")
def get_livestock():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT * FROM livestock")
    rows = c.fetchall()

    conn.close()

    return {"data": rows}

# ---------------- FARMS ----------------
@app.post("/add-farm")
def add_farm(farm: Farm):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO farms (name, income, cost)
        VALUES (?, ?, ?)
    """, (farm.name, farm.income, farm.cost))

    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.get("/farms")
def get_farms():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT * FROM farms")
    rows = c.fetchall()

    conn.close()

    return {"data": rows}
