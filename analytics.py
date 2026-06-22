from fastapi import APIRouter

router = APIRouter()

@router.get("/analytics/profit")
def profit():
    return {
        "revenue": [2, 3, 4, 6, 7, 8, 10],
        "cost": [1, 2, 2.5, 3, 4, 5, 6],
        "profit": [1, 1, 1.5, 3, 3, 3, 4]
    }
