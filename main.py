from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            income REAL,
            cost REAL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS livestock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_id INTEGER,
            name TEXT,
            type TEXT,
            weight REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- MODELS ----------------
class Farm(BaseModel):
    name: str
    income: float
    cost: float

class Livestock(BaseModel):
    farm_id: int
    name: str
    type: str
    weight: float

# ---------------- FARMS ----------------
@app.post("/farm/add")
def add_farm(farm: Farm):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO farms (name, income, cost) VALUES (?, ?, ?)",
        (farm.name, farm.income, farm.cost)
    )

    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.get("/farm/list")
def list_farms():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT * FROM farms")
    data = c.fetchall()

    conn.close()

    return {"data": data}

# ---------------- LIVESTOCK ----------------
@app.post("/livestock/add")
def add_livestock(item: Livestock):
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO livestock (farm_id, name, type, weight) VALUES (?, ?, ?, ?)",
        (item.farm_id, item.name, item.type, item.weight)
    )

    conn.commit()
    conn.close()

    return {"status": "ok"}

@app.get("/livestock/list")
def list_livestock():
    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT * FROM livestock")
    data = c.fetchall()

    conn.close()

    return {"data": data}

# ---------------- SHI CALC ----------------
@app.get("/shi/profit/{farm_id}")
def shi_profit(farm_id: int):

    conn = sqlite3.connect("farmwise.db")
    c = conn.cursor()

    c.execute("SELECT income, cost FROM farms WHERE id=?", (farm_id,))
    farm = c.fetchone()

    conn.close()

    if not farm:
        return {"status": "error"}

    income = farm[0]
    cost = farm[1]

    # SHI reduction simulation
    shi_saving = cost * 0.25
    final_cost = cost - shi_saving
    profit = income - final_cost

    return {
        "income": income,
        "cost": cost,
        "shi_saving": shi_saving,
        "final_profit": profit
    }
