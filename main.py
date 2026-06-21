from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "FarmWise Backend is running 🚀"}

@app.post("/ai/analyze")
def analyze(data: dict):
    return {
        "input": data,
        "result": "AI analysis completed",
        "model": "SHI-Engine",
        "profit_score": 87
    }
