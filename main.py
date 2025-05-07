from fastapi import FastAPI, Query, Body
from risk_utils import compute_risk_score
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()
app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Supply Chain Risk Detector API 👋",
        "docs": "/docs",
        "example": "/risk_score?supplier=China&product=semiconductor"
    }


@app.get("/risk_score")
def get_risk_score(supplier: str = Query(...), product: str = Query(...)):
    result = compute_risk_score(supplier, product)
    return result

@app.post("/batch_score")
def batch_score(
    items: List[Dict[str, str]] = Body(..., example=[
        {"supplier": "China", "product": "semiconductor"},
        {"supplier": "India", "product": "pharmaceuticals"}
    ])
):
    results = []
    for item in items:
        supplier = item.get("supplier")
        product = item.get("product")
        if supplier and product:
            result = compute_risk_score(supplier, product)
            results.append(result)
    return results
