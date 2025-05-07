from fastapi import FastAPI, Query
from risk_utils import compute_risk_score
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

@app.get("/risk_score")
def get_risk_score(supplier: str = Query(...), product: str = Query(...)):
    result = compute_risk_score(supplier, product)
    return result
