import streamlit as st
import requests
import pandas as pd

st.title("📦 Supply Chain Risk Detector")
st.markdown("Check geopolitical, disaster & economic risk for any supplier.")

supplier = st.text_input("Enter Supplier Country", "China")
product = st.text_input("Enter Product Type", "semiconductor")


# Interpretation helper
def interpret(score):
    if score < 0.35:
        return "🟢 Low"
    elif score < 0.7:
        return "🟡 Medium"
    else:
        return "🔴 High"

# Analyze Risk API call
if st.button("Analyze Risk"):
    url = "https://supply-chain-risk-api.onrender.com/risk_score"
    params = {"supplier": supplier, "product": product}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        st.success(f"📊 Total Risk Score: {data['risk_score']}")

        # ✅ Overall label
        overall_label = interpret(data["risk_score"])
        st.subheader("📊 Overall Risk Level")
        st.success(overall_label)

        # ✅ Predicted label from ML
        st.subheader("📌 Predicted News Risk Label")
        st.info(f"{data['risk_factors'].get('predicted_label', 'N/A')}")

        st.subheader("📰 Top News Summary")
        st.write(data['risk_factors'].get('summary', 'No summary available.'))

        st.subheader("🔗 Source Article")
        st.markdown(data['risk_factors'].get('explanation', 'No article link.'), unsafe_allow_html=True)

        # ✅ Explanation from model
        st.subheader("🧠 Explanation")
        st.write(data["risk_factors"].get("explanation", "No explanation available."))

        # ✅ Risk breakdown
        st.subheader("📉 Risk Breakdown")
        st.json({
            "News Risk": data["risk_factors"]["news_risk"],
            "Disaster Risk": data["risk_factors"]["natural_disaster_risk"],
            "Economic Risk": data["risk_factors"]["economic_risk"]
        })
    else:
        st.error("API call failed. Try again.")

# ---------------------------------------
# 📄 CSV Upload & Batch Scoring
# ---------------------------------------
st.markdown("---")
st.subheader("📄 Upload CSV for Batch Scoring")
uploaded_file = st.file_uploader("Upload a CSV file with 'supplier' and 'product' columns", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "supplier" in df.columns and "product" in df.columns:
        st.success(f"📦 Processing {len(df)} rows...")

        batch_data = df[["supplier", "product"]].to_dict(orient="records")

        try:
            response = requests.post("https://supply-chain-risk-api.onrender.com/batch_score", json=batch_data)
            if response.status_code == 200:
                results = response.json()
                results_df = pd.DataFrame(results)
                results_df["Risk Level"] = results_df["risk_score"].apply(interpret)

                st.dataframe(results_df[["supplier", "product", "risk_score", "Risk Level"]])
            else:
                st.error("❌ API request failed.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("CSV must have 'supplier' and 'product' columns.")
