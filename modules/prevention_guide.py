import streamlit as st

def run():
    st.header("🛡️ Disease Prevention Guide")

    prevention_categories = {
        "Hygiene & Sanitation": {
            "description": "Basic cleanliness practices to prevent disease spread",
            "practices": [
                "Clean milking equipment daily with approved sanitizers",
                "Maintain clean, dry bedding areas",
                "Regular cleaning of feed and water containers",
                "Proper waste management and disposal",
                "Hand hygiene for farm workers"
            ]
        },
        "Nutrition Management": {
            "description": "Proper feeding practices for disease prevention",
            "practices": [
                "Provide balanced nutrition based on life stage",
                "Ensure access to clean, fresh water",
                "Monitor body condition scores regularly",
                "Avoid sudden feed changes",
                "Store feed properly to prevent contamination"
            ]
        },
        "Vaccination Programs": {
            "description": "Essential vaccines for cattle health",
            "practices": [
                "Follow recommended vaccination schedules",
                "Consult veterinarian for regional disease risks",
                "Maintain proper vaccine storage conditions",
                "Keep detailed vaccination records",
                "Monitor for adverse reactions"
            ]
        },
        "Environmental Controls": {
            "description": "Managing the farm environment for health",
            "practices": [
                "Ensure proper ventilation in housing",
                "Control flies and other disease vectors",
                "Maintain appropriate stocking densities",
                "Provide adequate shelter from weather",
                "Regular facility maintenance and repair"
            ]
        }
    }

    for category, info in prevention_categories.items():
        with st.expander(f"📋 {category}"):
            st.markdown(f"**{info['description']}**")
            st.markdown("")
            for practice in info['practices']:
                st.markdown(f"• {practice}")
