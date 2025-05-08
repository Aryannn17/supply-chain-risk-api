import os
import requests
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
if not GNEWS_API_KEY:
    raise ValueError("⚠️ GNEWS_API_KEY not found in environment.")

QUERY = "supply chain OR export ban OR factory shutdown OR strike"
FROM_DATE = (datetime.utcnow() - timedelta(days=7)).date()
TO_DATE = datetime.utcnow().date()
MAX_ARTICLES = 50  # adjust as needed

url = f"https://gnews.io/api/v4/search?q={QUERY}&from={FROM_DATE}&to={TO_DATE}&lang=en&max=10&sortby=publishedAt&apikey={GNEWS_API_KEY}"

def fetch_articles():
    all_articles = []
    page = 1

    while len(all_articles) < MAX_ARTICLES:
        response = requests.get(url + f"&page={page}")
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break
        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            break

        for a in articles:
            all_articles.append({
                "title": a.get("title"),
                "description": a.get("description"),
                "content": a.get("content"),
                "publishedAt": a.get("publishedAt"),
                "url": a.get("url"),
                "risk_level": ""  # you’ll fill this manually later
            })

        page += 1

    return all_articles[:MAX_ARTICLES]

def save_to_csv(articles, filename="gnews_articles.csv"):
    keys = ["title", "description", "content", "publishedAt", "url", "risk_level"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(articles)
    print(f"✅ Saved {len(articles)} articles to {filename}")

if __name__ == "__main__":
    articles = fetch_articles()
    save_to_csv(articles)
