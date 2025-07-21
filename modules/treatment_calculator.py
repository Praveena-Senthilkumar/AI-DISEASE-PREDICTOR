import streamlit as st

def run():
    st.header("💊 Treatment Cost Calculator")

    disease_costs = {
        "Mastitis": {"mild": 1000, "moderate": 2000, "severe": 4000},
        "Lameness": {"mild": 1200, "moderate": 2500, "severe": 4500}
    }

    disease = st.selectbox("Disease", list(disease_costs.keys()))
    severity = st.selectbox("Severity", ["mild", "moderate", "severe"])
    num_animals = st.number_input("Number of Cattle", min_value=1, value=1)

    if disease and severity:
        cost = disease_costs[disease][severity] * num_animals
        st.subheader("📊 Cost Estimate")
        st.markdown(f"**Estimated Total Cost:** ₹{cost}")
        st.markdown(f"**Per Animal:** ₹{cost/num_animals}")
