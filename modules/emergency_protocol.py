import streamlit as st

def run():
    st.header("🚨 Emergency Protocol Guide")

    st.warning("⚠️ This emergency guide is for immediate first-response reference only. Always consult a licensed veterinarian as soon as possible.")

    st.markdown("This guide outlines how to identify and respond quickly to life-threatening or urgent conditions in cattle.")

    emergencies = {
        "Severe Bloat": {
            "symptoms": [
                "⚠️ Severe abdominal distension (left side especially)",
                "😰 Difficulty breathing or groaning",
                "💥 Sudden collapse or restlessness"
            ],
            "immediate_actions": [
                "🚶 Keep animal standing and walking",
                "🧪 Insert stomach tube if trained (to relieve gas buildup)",
                "📞 Call veterinarian immediately",
                "❌ Do NOT administer oral remedies unless directed",
                "👀 Monitor breathing and abdominal girth closely"
            ],
            "urgency": "🔴 CRITICAL – Act within minutes"
        },
        "Milk Fever Emergency": {
            "symptoms": [
                "🧊 Cold ears and limbs",
                "💤 Cow lying down and unable to stand",
                "💥 Muscle tremors or collapse after calving"
            ],
            "immediate_actions": [
                "🛏️ Provide soft bedding and keep animal calm",
                "📞 Contact veterinarian for IV calcium treatment",
                "🛑 Do not try to lift or force the cow to stand",
                "🌡️ Monitor vital signs if possible",
                "🧣 Keep cow warm and protected"
            ],
            "urgency": "🟠 URGENT – Act within 1–2 hours"
        }
        # Add more emergencies as needed...
    }

    for name, details in emergencies.items():
        with st.expander(f"🚨 {name}"):
            st.subheader(details["urgency"])
            st.markdown("### 🧿 Symptoms")
            for s in details["symptoms"]:
                st.markdown(f"- {s}")
            st.markdown("### 🛠️ Immediate Actions")
            for idx, a in enumerate(details["immediate_actions"], start=1):
                st.markdown(f"{idx}. {a}")
