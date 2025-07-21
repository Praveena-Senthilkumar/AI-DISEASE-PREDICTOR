import streamlit as st

def run(disease_db, treatment_db):
    st.header("🔍 Search Diseases")

    search_term = st.text_input("Enter disease name or symptom:", placeholder="e.g., mastitis, lameness, respiratory")

    if search_term:
        results = disease_db.search_diseases(search_term)

        if results:
            st.success(f"Found {len(results)} matching diseases:")

            for disease_name in results:
                with st.expander(f"🦠 {disease_name}"):
                    disease_info = disease_db.get_disease_info(disease_name)
                    treatment_info = treatment_db.get_treatment_info(disease_name)

                    if disease_info:
                        st.markdown(f"**Description:** {disease_info['description']}")
                        st.markdown(f"**Symptoms:** {disease_info['symptoms']}")

                        if treatment_info:
                            st.markdown(f"**Treatment:** {treatment_info['immediate_actions']}")
        else:
            st.info("No diseases found matching your search term. Try different keywords.")
