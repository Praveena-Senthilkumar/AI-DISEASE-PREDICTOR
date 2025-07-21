import streamlit as st

def run(disease_db, treatment_db):
    st.header("📚 Cow Disease Database")

    all_diseases = disease_db.get_all_diseases()
    
    if all_diseases:
        st.info(f"Database contains information on {len(all_diseases)} cow diseases")

        for disease_name in sorted(all_diseases.keys()):
            with st.expander(f"🦠 {disease_name}"):
                disease_info = all_diseases[disease_name]
                treatment_info = treatment_db.get_treatment_info(disease_name)

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("### Disease Information")
                    st.markdown(f"**Description:** {disease_info['description']}")
                    st.markdown(f"**Symptoms:** {disease_info['symptoms']}")
                    st.markdown(f"**Causes:** {disease_info['causes']}")
                    st.markdown(f"**Severity:** {disease_info.get('severity', 'Unknown')}")

                with col2:
                    if treatment_info:
                        st.markdown("### Treatment Information")
                        st.markdown(f"**Immediate Actions:** {treatment_info['immediate_actions']}")
                        st.markdown(f"**Medications:** {treatment_info['medications']}")
                        st.markdown(f"**Prevention:** {treatment_info['prevention']}")
    else:
        st.warning("Disease database is empty. Please check the database configuration.")
