# 🚚 Supply Chain Risk Detector API

An AI-powered FastAPI + Streamlit application that identifies **supply chain risks** based on:
- 📰 Real-time geopolitical news (via GNews)
- 🌍 Natural disaster likelihood by supplier region
- 📉 Country-level economic stability

This API helps organizations assess supplier reliability and flag sourcing risks before they escalate.

---

## 🔧 Features

- ✅ Real-time **news risk analysis** via weighted keyword extraction
- ✅ Country-specific **natural disaster likelihood** scoring
- ✅ Static **economic vulnerability scoring** using macroeconomic mapping
- ✅ **CSV batch scoring** support via API and Streamlit UI
- ✅ Fully deployed **REST API (FastAPI)** + **frontend dashboard (Streamlit)**
- ✅ Clean Swagger docs & public endpoints

---

## 🚀 Quick Start (Local Dev)

### 1. Clone the repository
```bash
git clone https://github.com/Aryannn17/supply-chain-risk-api.git
cd supply-chain-risk-api
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Set up .env file
Create a .env file in the root directory:
```
GNEWS_API_KEY=your_gnews_api_key_here
```
📝 You can get a free GNews API key from https://gnews.io

4. Run the API
```bash
uvicorn main:app --reload
```

Visit:
📍 http://127.0.0.1:8000/docs — for Swagger UI
📍 http://127.0.0.1:8000/risk_score?supplier=China&product=semiconductor — sample request

📈 Sample Response
{
  "supplier": "China",
  "product": "semiconductor",
  "risk_score": 0.5,
  "risk_factors": {
    "news_risk": 0.61,
    "natural_disaster_risk": 0.6,
    "economic_risk": 0.3
  }
}

🌐 Deployed Links
🔌 API: https://supply-chain-risk-api.onrender.com

🌐 Frontend: https://supply-chain-risk-api-lvwr9pd4jdhyej2ljm6spo.streamlit.app/

📄 Swagger: https://supply-chain-risk-api.onrender.com/docs


📦 Tech Stack
Backend: FastAPI, Requests, Uvicorn
Frontend: Streamlit, Pandas
Deployment: Render (API) + Streamlit Cloud
Data: GNews API + static disaster/economic mapping

🧠 Future Enhancements
⏳ Replace heuristics with ML/NLP scoring on news articles
🌍 Live disaster feeds (e.g., GDACS, ReliefWeb)
📈 Logging + analytics dashboard
🔐 API key system for public usage
📦 Package as SaaS microservice


🧑‍💻 Author
Built with ❤️ by Aryan Srivastva
📫 @Aryannn17
