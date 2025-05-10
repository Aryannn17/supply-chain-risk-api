import os
import requests

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

def get_news_risk(supplier_country, product):
    if not GNEWS_API_KEY:
        print("❌ Missing GNEWS_API_KEY")
        return 0.0

    query = f"{supplier_country} {product} risk OR disruption"
    url = f"https://gnews.io/api/v4/search?q={query}&lang=en&token={GNEWS_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        print(f"📰 Found {len(articles)} relevant articles.")
        return min(len(articles) / 20, 1.0)  # Normalize score to 0.0–1.0
    except Exception as e:
        print("Error fetching news:", e)
        return 0.0
