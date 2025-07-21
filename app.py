import streamlit as st
from user_database import init_db, verify_user, create_user

# Load shared resources
@st.cache_resource
def load_resources():
    from disease_database import DiseaseDatabase
    from treatment_database import TreatmentDatabase
    from image_processor import ImageProcessor
    from ml_model import CowDiseaseModel
    disease_db = DiseaseDatabase()
    treatment_db = TreatmentDatabase()
    image_processor = ImageProcessor()
    ml_model = CowDiseaseModel()
    return disease_db, treatment_db, image_processor, ml_model


# Import your modular page functions
from modules import (
    diagnosis,
    disease_database,
    search_diseases,
    treatment_calculator,
    emergency_protocol,
    prevention_guide,
    find_vet
)

# Initialize user DB
init_db()

# ------------------ SESSION STATE INIT ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ------------------ LOGIN PAGE ------------------
def show_login():
    st.set_page_config(page_title="Pashu Raksha Login", layout="centered")
    st.title("🐄 Pashu Raksha")
    st.markdown("### 👋 Welcome! Please log in to continue.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("🔐 Log In"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.markdown("Don't have an account?")
    if st.button("📝 Sign Up"):
        st.session_state.show_signup = True
        st.rerun()

# ------------------ SIGNUP PAGE ------------------
def show_signup():
    st.set_page_config(page_title="Pashu Raksha Signup", layout="centered")
    st.title("🔐 Create a New Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("✅ Sign Up"):
        if new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif create_user(new_user, new_pass):
            st.success("Account created! Please log in.")
            st.session_state.show_signup = False
            st.rerun()
        else:
            st.error("Username already exists.")

    st.markdown("Already have an account?")
    if st.button("🔙 Back to Login"):
        st.session_state.show_signup = False
        st.rerun()

# ------------------ MAIN DASHBOARD ------------------
def show_dashboard():
    st.set_page_config(page_title="Moocare", layout="wide")
    st.title("🐄 Moocare Dashboard")
   

    # ✅ Load all shared resources once
    disease_db, treatment_db, image_processor, ml_model = load_resources()


    # Sidebar account section
    st.sidebar.title("👤 Account")
    st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")

    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully.")
        st.rerun()

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Home",
        "Diagnosis",
        "Disease Database",
        "Search Diseases",
        "Treatment Calculator",
        "Emergency Protocols",
        "Prevention",
        "Find a Vet"
    ])

    # Welcome Message
    st.markdown(f"### 👋 Welcome, **{st.session_state.username}**")

    # Page routing
    if page == "Home":
        st.subheader("🐄 Welcome to Pashu Raksha")
        st.markdown("Use the sidebar to navigate through the features.")
    elif page == "Diagnosis":
        diagnosis.run(disease_db, treatment_db, image_processor, ml_model)
    elif page == "Disease Database":
        disease_database.run(disease_db, treatment_db)
    elif page == "Search Diseases":
        search_diseases.run(disease_db, treatment_db)
    elif page == "Treatment Calculator":
        treatment_calculator.run(disease_db, treatment_db)
    elif page == "Emergency Protocols":
        emergency_protocol.run(disease_db, treatment_db)
    elif page == "Prevention":
        prevention_guide.run(disease_db, treatment_db)
    elif page == "Find a Vet":
        find_vet.run()
    else:
        st.error("🚫 Page not found. Please select a valid page from the sidebar.")

# ------------------ ENTRY POINT ------------------
if __name__ == "__main__":
    if not st.session_state.logged_in:
        if st.session_state.show_signup:
            show_signup()
        else:
            show_login()
    else:
        show_dashboard()
