from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "FarmWise Backend Live 🚀"}

@app.post("/login")
def login(data: dict):
    return {
        "token": "demo_token_123",
        "role": "admin"
    }

@app.get("/analytics/profit")
def profit():
    return {
        "revenue": [2, 3, 4, 6, 7, 8, 10],
        "cost": [1, 2, 2.5, 3, 4, 5, 6],
        "profit": [1, 1, 1.5, 3, 3, 3, 4]
    }

@app.post("/ai/analyze")
def ai(data: dict):
    return {
        "result": "AI analysis OK",
        "score": 87
    }