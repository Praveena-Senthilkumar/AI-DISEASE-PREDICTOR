import streamlit as st
import pandas as pd

def run(db_manager):
    st.header("📊 Health Analytics Dashboard")
    st.info("Track your herd's health patterns and trends")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Diagnoses", "47", "12%")
    with col2:
        st.metric("Most Common Disease", "Mastitis", "35% of cases")
    with col3:
        st.metric("Prevention Success Rate", "78%", "5%")

    st.subheader("📈 Disease Frequency Trends (Mock)")
    st.info("Health analytics requires connection to your farm management system or manual data entry to display real trends and statistics.")

    st.subheader("📝 Manual Health Record Entry")
    with st.form("health_record_form"):
        col1, col2 = st.columns(2)
        with col1:
            cow_id = st.text_input("Cow ID/Tag Number")
            diagnosis_date = st.date_input("Diagnosis Date")
            disease = st.selectbox("Diagnosed Disease", ["Mastitis", "Lameness", "Respiratory Disease", "Ketosis", "Pink Eye", "Other"])
        with col2:
            severity = st.selectbox("Severity Level", ["Mild", "Moderate", "Severe"])
            cost = st.number_input("Treatment Cost (₹)", min_value=0.0)
            vet = st.text_input("Veterinarian Name")
        notes = st.text_area("Additional Notes")
        submitted = st.form_submit_button("Add Health Record")

        if submitted and cow_id and disease:
            record_data = {
                'cow_id': cow_id,
                'diagnosis_date': diagnosis_date,
                'disease_name': disease,
                'severity': severity.lower(),
                'treatment_applied': f"{severity} treatment for {disease}",
                'total_cost': cost,
                'veterinarian': vet,
                'notes': notes
            }
            if db_manager.add_health_record(record_data):
                st.success(f"Health record added for Cow {cow_id}")
            else:
                st.error("Failed to save record")
