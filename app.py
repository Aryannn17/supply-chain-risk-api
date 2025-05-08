import streamlit as st
import requests
import pandas as pd


st.title("📦 Supply Chain Risk Detector")

st.markdown("Check geopolitical, disaster & economic risk for any supplier.")

supplier = st.text_input("Enter Supplier Country", "China")
product = st.text_input("Enter Product Type", "semiconductor")

if st.button("Analyze Risk"):
    url = "https://supply-chain-risk-api.onrender.com/risk_score"
    params = {"supplier": supplier, "product": product}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        st.success(f"Total Risk Score: {data['risk_score']}")
        st.subheader("Breakdown:")
        st.json(data["risk_factors"])
    else:
        st.error("API call failed. Try again.")

st.markdown("---")
st.subheader("📄 Upload CSV for Batch Scoring")

uploaded_file = st.file_uploader("Upload a CSV file with 'supplier' and 'product' columns", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    if "supplier" in df.columns and "product" in df.columns:
        st.success(f"📦 Processing {len(df)} rows...")

        # Convert to list of dicts
        batch_data = df[["supplier", "product"]].to_dict(orient="records")

        # Send to /batch_score
        try:
            response = requests.post("https://supply-chain-risk-api.onrender.com/batch_score", json=batch_data)
            if response.status_code == 200:
                results = response.json()
                results_df = pd.DataFrame(results)

# Add interpretation
def interpret(score):
    if score < 0.35:
        return "🟢 Low"
    elif score < 0.7:
        return "🟡 Medium"
    else:
        return "🔴 High"

results_df["Risk Level"] = results_df["risk_score"].apply(interpret)

# Show styled table
st.dataframe(results_df[["supplier", "product", "risk_score", "Risk Level"]])

            else:
                st.error("❌ API request failed.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("CSV must have 'supplier' and 'product' columns.")
