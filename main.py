<<<<<<< HEAD
﻿from fastapi import FastAPI
=======
from fastapi import FastAPI
>>>>>>> b53d9d90fc91fba95f2a872a0e5a58e34fe4a3b7

app = FastAPI()

@app.get("/")
def home():
    return {"status": "FarmWise Backend is running 🚀"}

@app.post("/ai/analyze")
def analyze(data: dict):
    return {
        "input": data,
        "result": "AI analysis completed",
        "profit_score": 87,
<<<<<<< HEAD
        "recommendation": "Use SHI protein instead of 20% soybean meal"
=======
        "recommendation": "Use SHI protein instead of soybean"
>>>>>>> b53d9d90fc91fba95f2a872a0e5a58e34fe4a3b7
    }
