import os
import requests
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ✅ Load GNews API key
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# ✅ Load trained ML model
model = joblib.load("news_risk_model.pkl")

# ✅ Label-to-score mapping
LABEL_TO_SCORE = {
    "Low": 0.2,
    "Medium": 0.5,
    "High": 0.8
}

# ✅ 1. News Risk (ML-based)
def get_news_risk(supplier, product):
    query = f"{supplier} {product}"
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=7)

    url = (
        f"https://gnews.io/api/v4/search?q={query}"
        f"&from={from_date.date()}&to={to_date.date()}"
        f"&lang=en&max=10&sortby=publishedAt&apikey={GNEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])

    if not articles:
        return 0.2, {
            "predicted_label": "Low",
            "explanation": "No recent news articles found."
        }

    # Use first article for scoring (or combine later if needed)
    texts = [a['title'] + " " + a.get('description', '') for a in articles]
    predicted_labels = model.predict(texts)
    label_counts = pd.Series(predicted_labels).value_counts()
    # Choose most frequent label
    top_label = label_counts.idxmax()
    score = LABEL_TO_SCORE.get(top_label, 0.5)

    return round(score, 2), {
        "predicted_label": predicted_label,
        "explanation": f"Predicted '{predicted_label}' risk based on recent article: '{articles[0]['title']}'"
    }

# ✅ 2. Natural Disaster Risk
def get_natural_disaster_risk(supplier: str) -> float:
    high_risk_countries = ["Philippines", "Indonesia", "Bangladesh", "Nepal", "China", "India"]
    return 0.6 if supplier in high_risk_countries else 0.2

# ✅ 3. Economic Risk
def get_economic_risk(supplier: str) -> float:
    economic_risk_map = {
        "China": 0.3,
        "India": 0.4,
        "USA": 0.1,
        "Russia": 0.6,
        "Germany": 0.2,
        "Sri Lanka": 0.8,
        "Pakistan": 0.7
    }
    return economic_risk_map.get(supplier, 0.5)

# ✅ 4. Final Risk Scoring
def compute_risk_score(supplier, product):
    news_risk, news_meta = get_news_risk(supplier, product)
    natural_disaster_risk = get_natural_disaster_risk(supplier)
    economic_risk = get_economic_risk(supplier)

    total_risk = round((news_risk + natural_disaster_risk + economic_risk) / 3, 2)

    return {
        "supplier": supplier,
        "product": product,
        "risk_score": total_risk,
        "risk_factors": {
            "news_risk": news_risk,
            "natural_disaster_risk": natural_disaster_risk,
            "economic_risk": economic_risk,
            "predicted_label": news_meta["predicted_label"],
            "explanation": news_meta["explanation"]
        }
    }
