import requests
from datetime import datetime, timedelta

# GNews API setup
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

RISK_KEYWORDS = {
    "conflict": 0.9,
    "ban": 0.8,
    "war": 1.0,
    "sanction": 0.7,
    "shortage": 0.6,
    "strike": 0.6,
    "disruption": 0.7,
    "protest": 0.5,
    "tariff": 0.4
}

# ✅ 1. News Risk
def get_news_risk(supplier, product):
    query = f"{supplier} {product}"
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=7)

    url = f"https://gnews.io/api/v4/search?q={query}&from={from_date.date()}&to={to_date.date()}&lang=en&apikey={GNEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        return 0.0

    keyword_hits = 0
    total_weight = 0
    for article in articles:
        content = f"{article['title']} {article.get('description', '')}".lower()
        for word, weight in RISK_KEYWORDS.items():
            if word in content:
                keyword_hits += 1
                total_weight += weight

    normalized_score = min(total_weight / len(articles), 1.0)
    return round(normalized_score, 2)

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
    news_risk = get_news_risk(supplier, product)
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
            "economic_risk": economic_risk
        }
    }
