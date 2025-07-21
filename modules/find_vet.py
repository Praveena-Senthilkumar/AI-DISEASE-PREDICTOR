import streamlit as st

def run():
    st.header("🏥 Find Veterinarian")

    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Your Location (City/ZIP)")
        service = st.selectbox("Service Type", [
            "General Veterinary Care", "Emergency", "Nutrition", "Reproduction", "Large Animal Specialist"
        ])
    with col2:
        radius = st.slider("Search Radius (km)", 5, 50, 20)
        availability = st.selectbox("Availability", ["Any time", "24/7", "Weekdays", "Weekends"])

    if st.button("Search Veterinarians") and location:
        st.info("Mock data. Integration with real vet directories pending.")
        st.subheader("Sample Veterinarians")
        for vet in [
            {"name": "Dr. Sarah Johnson", "clinic": "Farm Animal Care", "phone": "1234567890", "distance": "8 km"},
            {"name": "Dr. Ramesh B", "clinic": "Green Valley Vet", "phone": "9876543210", "distance": "12 km"}
        ]:
            with st.expander(f"{vet['name']} - {vet['clinic']}"):
                st.markdown(f"**Phone:** {vet['phone']}  \n**Distance:** {vet['distance']}")
