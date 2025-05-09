import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load labeled dataset
df = pd.read_csv("gnews_articles.csv")

# Combine relevant text fields
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("") + " " + df["content"].fillna("")

# Drop rows with missing labels
df = df[df["risk_level"].notna()]

# Features and labels
X = df["text"]
y = df["risk_level"]

# Create a text classification pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", LogisticRegression(max_iter=1000))
])

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "news_risk_model.pkl")
print("✅ Model trained and saved as news_risk_model.pkl")
