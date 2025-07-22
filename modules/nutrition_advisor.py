import streamlit as st
import ast
from cow_nutrition_model.suggest import get_nutrition_advice

def run():
    st.title("🐄 Nutrition Advisor for Livestock")

    # User input
    breed = st.selectbox("🔸 Select Breed", ["Select", "Jersey", "Gir", "HF", "Sahiwal", "Other"])
    age = st.number_input("🔸 Enter Age (in years)", min_value=0.0, step=0.1)
    stage = st.selectbox("🔸 Select Stage", ["Select", "Calf", "Growing", "Adult", "Pregnant", "Lactating", "Dry", "Senior"])

    if st.button("✅ Get Nutrition Advice"):
        if breed == "Select" or stage == "Select" or age <= 0:
            st.warning("⚠️ Please select valid Breed, Age (> 0), and Stage.")
            return

        result = get_nutrition_advice(breed, age, stage)

        # Convert to dictionary if result is a string
        if isinstance(result, str):
            try:
                result = ast.literal_eval(result)
            except Exception as e:
                st.error(f"⚠️ Error decoding advice: {e}")
                return

        # Show results in visible cards
        st.markdown("---")
        st.subheader("📋 Personalized Nutrition Plan")

        st.markdown(f"""
        <div style="background-color:#f9f9f9; padding:15px; border-radius:12px; margin-bottom:15px;">
            <h4>🥗 Nutrition</h4>
            <p>{result.get("nutrition", "-")}</p>
        </div>

        <div style="background-color:#f0f8ff; padding:15px; border-radius:12px; margin-bottom:15px;">
            <h4>🌾 Food</h4>
            <p>{result.get("food", "-")}</p>
        </div>

        <div style="background-color:#fff0f5; padding:15px; border-radius:12px; margin-bottom:15px;">
            <h4>💊 Supplements</h4>
            <p>{result.get("supplements", "-")}</p>
        </div>

        <div style="background-color:#e6ffe6; padding:15px; border-radius:12px; margin-bottom:15px;">
            <h4>🛠 Remedies</h4>
            <p>{result.get("remedies", "-")}</p>
        </div>

        <div style="background-color:#fffbe6; padding:15px; border-radius:12px;">
            <h4>📅 Follow-Up Plan</h4>
            <p>{result.get("follow_up", "-")}</p>
        </div>
        """, unsafe_allow_html=True)
