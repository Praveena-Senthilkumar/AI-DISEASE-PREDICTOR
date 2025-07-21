import streamlit as st
from user_database import init_db, create_user, verify_user

from modules import (
    diagnosis,
    disease_database,
    search_diseases,
    treatment_calculator,
    emergency_protocol,
    prevention_guide,
    find_vet
)

def back_to_home_button(texts):
    if st.button("🔙 " + texts["home"]):
        st.session_state.page = texts["home"]
        st.rerun()


LANGUAGES = {
    "English": {
        "login_title": "🐄 Pashu Raksha Login",
        "welcome": "Welcome",
        "username": "Username",
        "password": "Password",
        "login": "Log In",
        "signup": "Sign Up",
        "no_account": "Don't have an account?",
        "have_account": "Already have an account?",
        "logout": "Logout",
        "account": "Account",
        "navigation": "Navigation",
        "choose_page": "Choose a page",
        "language": "Language",
        "settings": "Settings",
        "font_size": "Font Size",
        "home": "Home",
        "login_success": "✅ Login successful!",
        "logout_success": "✅ Logged out successfully!",
        "invalid": "❌ Invalid username or password.",
        "signup_success": "✅ Signup successful. Please login!",
        "signup_error": "❌ Username already exists.",
        "logged_in_as": "Logged in as",
        "diagnosis": "Diagnosis",
        "disease_db": "Disease Database",
        "search": "Search Diseases",
        "calculator": "Treatment Calculator",
        "emergency": "Emergency Protocols",
        "prevention": "Prevention",
        "find_vet": "Find a Vet"
    },
    "தமிழ்": {
        "login_title": "🐄 பசு ரக்ஷா உள்நுழைவு",
        "welcome": "வரவேற்பு",
        "username": "பயனர்பெயர்",
        "password": "கடவுச்சொல்",
        "login": "உள்நுழை",
        "signup": "பதிவுசெய்",
        "no_account": "கணக்கு இல்லையா?",
        "have_account": "ஏற்கனவே கணக்கு உள்ளதா?",
        "logout": "வெளியேறு",
        "account": "கணக்கு",
        "navigation": "வழிசெலுத்தல்",
        "choose_page": "பக்கத்தை தேர்ந்தெடு",
        "language": "மொழி",
        "settings": "அமைப்புகள்",
        "font_size": "எழுத்து அளவு",
        "home": "முகப்பு",
        "login_success": "✅ உள்நுழைவு வெற்றிகரமாக முடிந்தது!",
        "logout_success": "✅ வெற்றிகரமாக வெளியேறியது!",
        "invalid": "❌ தவறான பயனர்பெயர் அல்லது கடவுசொல்.",
        "signup_success": "✅ பதிவு வெற்றிகரமாக முடிந்தது. தயவுசெய்து உள்நுழைக!",
        "signup_error": "❌ பயனர்பெயர் ஏற்கனவே உள்ளது.",
        "logged_in_as": "உள்நுழைந்தவர்",
        "diagnosis": "நோயறிதல்",
        "disease_db": "நோய் தரவுத்தொகுப்பு",
        "search": "நோய்கள் தேடு",
        "calculator": "சிகிச்சை கணிப்பான்",
        "emergency": "அவசர நெறிமுறைகள்",
        "prevention": "முன்கூட்டிய தடுப்பு",
        "find_vet": "வெட்னரியை காண்க"
    },
    "हिन्दी": {
        "login_title": "🐄 पशु रक्षा लॉगिन",
        "welcome": "स्वागत है",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "login": "लॉग इन",
        "signup": "साइन अप",
        "no_account": "अकाउंट नहीं है?",
        "have_account": "पहले से अकाउंट है?",
        "logout": "लॉगआउट",
        "account": "खाता",
        "navigation": "नेविगेशन",
        "choose_page": "पृष्ठ चुनें",
        "language": "भाषा",
        "settings": "सेटिंग्स",
        "font_size": "फ़ॉन्ट साइज",
        "home": "मुख्यपृष्ठ",
        "login_success": "✅ लॉगिन सफल!",
        "logout_success": "✅ लॉगआउट सफल!",
        "invalid": "❌ गलत यूज़रनेम या पासवर्ड।",
        "signup_success": "✅ साइनअप सफल! कृपया लॉगिन करें।",
        "signup_error": "❌ यूज़रनेम पहले से मौजूद है।",
        "logged_in_as": "लॉग इन उपयोगकर्ता",
        "diagnosis": "बीमारी का विश्लेषण",
        "disease_db": "बीमारी डेटाबेस",
        "search": "बीमारियाँ खोजें",
        "calculator": "उपचार कैलकुलेटर",
        "emergency": "आपातकालीन प्रोटोकॉल",
        "prevention": "रोकथाम",
        "find_vet": "पशु चिकित्सक खोजें"
    }
}

# ---------------- Session Init ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "language" not in st.session_state:
    st.session_state.language = "English"
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False

# ---------------- Shared Resource Loader ----------------
@st.cache_resource
def load_resources():
    from disease_database import DiseaseDatabase
    from treatment_database import TreatmentDatabase
    from image_processor import ImageProcessor
    from ml_model import CowDiseaseModel
    return DiseaseDatabase(), TreatmentDatabase(), ImageProcessor(), CowDiseaseModel()

# ---------------- Login & Signup ----------------
def show_login(texts):
    st.set_page_config(page_title=texts["login_title"], layout="centered")
    st.title(texts["login_title"])
    username = st.text_input(texts["username"])
    password = st.text_input(texts["password"], type="password")

    if st.button(f"🔐 {texts['login']}"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(texts["login_success"])
            st.rerun()
        else:
            st.error(texts["invalid"])

    if st.button(f"📝 {texts['signup']}"):
        st.session_state.signup_mode = True
        st.rerun()

def show_signup(texts):
    st.set_page_config(page_title=texts["signup"], layout="centered")
    st.title(f"📝 {texts['signup']}")
    username = st.text_input(texts["username"])
    password = st.text_input(texts["password"], type="password")

    if st.button(f"✅ {texts['signup']}"):
        if create_user(username, password):
            st.success(texts["signup_success"])
            st.session_state.signup_mode = False
        else:
            st.error(texts["signup_error"])

    if st.button(f"🔙 {texts['login']}"):
        st.session_state.signup_mode = False
        st.rerun()

# ---------------- Dashboard ----------------
def show_dashboard(texts):
    st.set_page_config(page_title="Pashu Raksha", layout="wide")

    st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #F8FAFC;
    }
    </style>
""", unsafe_allow_html=True)


    # Sidebar
    with st.sidebar:
        st.markdown(f"## 👤 {texts['account']}")
        st.markdown(f"{texts['logged_in_as']}: **{st.session_state.username}**")

        if st.button(f"🔓 {texts['logout']}"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success(texts["logout_success"])
            st.rerun()

        st.markdown("---")
        st.markdown(f"## 🌐 {texts['language']}")
        st.session_state.language = st.selectbox(
            "", list(LANGUAGES.keys()), index=list(LANGUAGES).index(st.session_state.language)
        )

        st.markdown(f"## ⚙️ {texts['settings']}")
        font_size = st.radio(f"{texts['font_size']}", ["Small", "Medium", "Large"], index=1)

        font_css = {
            "Small": "14px",
            "Medium": "17px",
            "Large": "20px"
        }
        st.markdown(f"""
            <style>
            html, body, [class*="css"]  {{
                font-size: {font_css[font_size]} !important;
            }}
            </style>
        """, unsafe_allow_html=True)


    texts = LANGUAGES[st.session_state.language]
    st.markdown(f"### 👋 {texts['welcome']}, **{st.session_state.username}**")

    disease_db, treatment_db, image_processor, ml_model = load_resources()

    if st.session_state.page == texts["home"]:
        st.markdown("### ✨ Choose a feature to continue:")

        st.markdown(f"""
            <style>
            .grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
                padding: 10px 0;
            }}
            .card {{
                background-color: #ffffff;
                border-radius: 15px;
                width: 250px;
                height: 140px;
                padding: 20px;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                text-align: center;
                font-size: 1.1rem;
            }}
            .card:hover {{
                transform: scale(1.05);
                background-color: #f0f8ff;
                cursor: pointer;
            }}
            @media (max-width: 768px) {{
                .grid {{ flex-direction: column; align-items: center; }}
            }}
            </style>
        """, unsafe_allow_html=True)

        features = [
            (texts["diagnosis"], "🧪", "Diagnosis"),
            (texts["disease_db"], "📚", "Disease Database"),
            (texts["search"], "🔍", "Search Diseases"),
            (texts["calculator"], "🧮", "Treatment Calculator"),
            (texts["emergency"], "🚨", "Emergency Protocols"),
            (texts["prevention"], "🛡️", "Prevention"),
            (texts["find_vet"], "🩺", "Find a Vet"),
        ]

        st.markdown('<div class="grid">', unsafe_allow_html=True)
        for label, emoji, page_key in features:
            if st.button(f"{emoji} {label}", key=label):
                st.session_state.page = page_key
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "Diagnosis":
        back_to_home_button(texts)
        diagnosis.run(disease_db, treatment_db, image_processor, ml_model)
       
    elif st.session_state.page == "Disease Database":
        back_to_home_button(texts)
        disease_database.run(disease_db, treatment_db)
        
    elif st.session_state.page == "Search Diseases":
        back_to_home_button(texts)
        search_diseases.run(disease_db, treatment_db)
        
    elif st.session_state.page == "Treatment Calculator":
        back_to_home_button(texts)
        treatment_calculator.run(disease_db, treatment_db)
       
    elif st.session_state.page == "Emergency Protocols":
        back_to_home_button(texts)
        emergency_protocol.run(disease_db, treatment_db)
        
    elif st.session_state.page == "Prevention":
        back_to_home_button(texts)
        prevention_guide.run(disease_db, treatment_db)
        
    elif st.session_state.page == "Find a Vet":
        back_to_home_button(texts)
        find_vet.run()
        

# ---------------- Main Entry ----------------
if __name__ == "__main__":
    init_db()
    texts = LANGUAGES[st.session_state.language]

    if not st.session_state.logged_in:
        if st.session_state.signup_mode:
            show_signup(texts)
        else:
            show_login(texts)
    else:
        show_dashboard(texts)
