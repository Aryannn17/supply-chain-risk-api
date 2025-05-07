# Supply Chain Risk Detector API 🚚📉

An AI-driven FastAPI application that identifies **supply chain risks** based on:
- Real-time geopolitical news
- Regional natural disaster profiles
- Country-level economic instability

This API helps businesses assess the reliability of their suppliers before making critical sourcing decisions.

---

## 🔧 Features

✅ Real-time **news-based risk analysis** via GNews API  
✅ Country-based **natural disaster likelihood** scoring  
✅ Economic vulnerability scoring via **static risk map**  
✅ Clean JSON API built with **FastAPI**  
✅ Easily extendable and production-ready

---

## 🚀 Quick Start

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

🧑‍💻 Author
Built with ❤️ by Aryan Srivastva
📫 @Aryannn17
