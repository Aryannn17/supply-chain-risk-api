import streamlit as st
import requests

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
