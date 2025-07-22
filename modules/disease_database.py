import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import datetime
import smtplib
from email.message import EmailMessage

# ---------- Function to generate PDF ----------
def generate_pdf(disease_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Cow Disease Database", ln=True, align='C')
    pdf.set_font("Arial", size=11)

    for disease in disease_data:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt=f"🦠 {disease['Disease Name']}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, f"📝 Description: {disease['Description']}")
        pdf.multi_cell(0, 10, f"⚠️ Symptoms: {disease['Symptoms']}")
        pdf.multi_cell(0, 10, f"🧫 Causes: {disease['Causes']}")
        pdf.multi_cell(0, 10, f"📊 Severity: {disease['Severity']}")
        pdf.multi_cell(0, 10, f"🚑 Immediate Actions: {disease['Immediate Actions']}")
        pdf.multi_cell(0, 10, f"💊 Medications: {disease['Medications']}")
        pdf.multi_cell(0, 10, f"🛡️ Prevention: {disease['Prevention']}")
        pdf.ln(5)

    return pdf.output(dest="S").encode("latin-1")


# ---------- Function to send feedback via email ----------
def send_feedback_email(disease_name, issue_description):
    try:
        sender = st.secrets["email"]["sender"]
        receiver = st.secrets["email"]["receiver"]
        app_password = st.secrets["email"]["app_password"]

        msg = EmailMessage()
        msg["Subject"] = f"🧾 Feedback Report for: {disease_name}"
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(
            f"Feedback submitted for disease: {disease_name}\n\nIssue or Suggestion:\n{issue_description}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email Error:", e)
        return False


# ---------- Main App Function ----------
def run(disease_db, treatment_db):
    # ---------- CSS ----------
    st.markdown(
        """
        <style>
        .back-home {
            float: right;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            padding: 6px 12px;
            border: none;
            border-radius: 5px;
            text-decoration: none;
        }
        .card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 10px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
            color: #2e7d32;
        }
        .section-sub {
            font-weight: 600;
            color: #444;
        }
        .print-button {
            background-color: #0288d1;
            color: white;
            padding: 8px 14px;
            border: none;
            border-radius: 8px;
            font-size: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<a href="/" class="back-home">🏠 Home</a>', unsafe_allow_html=True)
    st.header("📚 Cow Disease Database")
    st.caption(f"🕒 Last Updated: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}")

    all_diseases = disease_db.get_all_diseases()
    if not all_diseases:
        st.warning("Disease database is empty. Please check the database configuration.")
        return

    search_term = st.text_input("🔎 Search Disease", "")
    filtered_diseases = {
        name: info for name, info in all_diseases.items()
        if search_term.lower() in name.lower()
    }

    st.info(f"Displaying {len(filtered_diseases)} of {len(all_diseases)} diseases")

    disease_list = []
    for name, info in filtered_diseases.items():
        treatment = treatment_db.get_treatment_info(name) or {}
        disease_list.append({
            "Disease Name": name,
            "Description": info.get("description", ""),
            "Symptoms": info.get("symptoms", ""),
            "Causes": info.get("causes", ""),
            "Severity": info.get("severity", "Unknown"),
            "Immediate Actions": treatment.get("immediate_actions", ""),
            "Medications": treatment.get("medications", ""),
            "Prevention": treatment.get("prevention", "")
        })

    if st.button("⬇️ Download CSV"):
        df = pd.DataFrame(disease_list)
        st.download_button("📥 Click to Download CSV", df.to_csv(index=False), "cow_diseases.csv", "text/csv")

    if st.button("⬇️ Download PDF"):
        pdf_data = generate_pdf(disease_list)
        b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        pdf_link = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="cow_diseases.pdf">📄 Click to Download PDF</a>'
        st.markdown(pdf_link, unsafe_allow_html=True)

    st.markdown("""
        <script>
        function printPage() {
            window.print();
        }
        </script>
        <button class="print-button" onclick="printPage()">🖨️ Print This Page</button>
        """, unsafe_allow_html=True)

    for disease_name in sorted(filtered_diseases.keys()):
        with st.expander(f"🦠 {disease_name}"):
            disease_info = filtered_diseases[disease_name]
            treatment_info = treatment_db.get_treatment_info(disease_name)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Disease Information</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="section-sub">📝 Description:</div> {disease_info["description"]}', unsafe_allow_html=True)
                st.markdown(f'<div class="section-sub">⚠️ Symptoms:</div> {disease_info["symptoms"]}', unsafe_allow_html=True)
                st.markdown(f'<div class="section-sub">🧫 Causes:</div> {disease_info["causes"]}', unsafe_allow_html=True)
                st.markdown(f'<div class="section-sub">📊 Severity:</div> {disease_info.get("severity", "Unknown")}', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                if treatment_info:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">Treatment Information</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-sub">🚑 Immediate Actions:</div> {treatment_info["immediate_actions"]}', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-sub">💊 Medications:</div> {treatment_info["medications"]}', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-sub">🛡️ Prevention:</div> {treatment_info["prevention"]}', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ Treatment information not found for this disease.")

    # ---------- Feedback Feature ----------
    st.markdown("---")
    with st.expander("⚠️ Report Incorrect Information or Suggest Updates"):
        reported_disease = st.text_input("🔧 Disease name you're reporting:")
        issue_desc = st.text_area("🗒️ Describe the issue or your suggestion:")
        
        if st.button("📩 Submit Feedback"):
            if reported_disease and issue_desc:
                if send_feedback_email(reported_disease, issue_desc):
                    st.success("✅ Feedback submitted and email sent to admin!")
                else:
                    st.error("❌ Failed to send email. Please try again later.")
            else:
                st.warning("Please fill in both fields before submitting.")
