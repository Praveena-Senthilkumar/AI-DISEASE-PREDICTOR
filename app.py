import streamlit as st
import pandas as pd
from PIL import Image
import time
import io
import os
from datetime import datetime, date
from disease_database import DiseaseDatabase
from treatment_database import TreatmentDatabase
from image_processor import ImageProcessor
from ml_model import CowDiseaseModel
from database import get_database_manager
from user_database import init_db, create_user, verify_user
init_db()  # Initializes DB when app starts

import streamlit as st

# Set page configuration
st.set_page_config(page_title="Cattle diesease analyser", page_icon="🐄", layout="centered")

# Set light grey background for entire login page
st.markdown("""
    <style>
    body {
        background-color: #f2f2f2;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Dummy credentials
USER_CREDENTIALS = {
    "admin": "pass123",
    "vet": "pashu2025"
}

def login():
    st.markdown("""
    <div style='text-align: center; padding-bottom: 20px;'>
        <h2 style='margin-bottom: 0;'>🐄 "Healthy cattle, happy homes"</h2>
        <h3 style='margin-top: 5px;'>Welcome to <strong>Pashu Raksha</strong></h3>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Email / Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("LOG IN")

    if login_btn:
        with st.spinner("Logging in..."):
            time.sleep(1.5)  # Simulate server-side delay (optional)
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")


    st.markdown('<small>Forgot password</small>', unsafe_allow_html=True)
    st.markdown('<small>Didn’t have an account?</small>', unsafe_allow_html=True)

    # Initialize temporary user "database" in session_state
    if "user_db" not in st.session_state:
        st.session_state.user_db = {
            "admin": "pass123",
            "vet": "pashu2025"
        }

    if st.button("Sign up"):
        st.session_state.show_signup = True
        st.rerun()

    # Signup Form Logic
    if st.session_state.get("show_signup", False):
        st.markdown("---")
        st.subheader("🔐 Create a New Account")
        new_user = st.text_input("Choose a username")
        new_pass = st.text_input("Choose a password", type="password")
        confirm_pass = st.text_input("Confirm password", type="password")
        create_btn = st.button("Create Account")

        if create_btn:
            if not new_user or not new_pass or not confirm_pass:
                st.warning("⚠️ All fields are required!")
            elif new_pass != confirm_pass:
                st.warning("❌ Passwords do not match.")
            elif create_user(new_user, new_pass):
                st.success("✅ Account created successfully! You can now log in.")
                st.session_state.show_signup = False
            else:
                st.error("🚫 Username already exists!")


    st.markdown("""
        <div style='text-align:center; padding-top: 20px;'>
            <img src="https://t4.ftcdn.net/jpg/05/92/17/11/360_F_592171170_c4As1Gfbpfl1r1KjnJm4oiyf1xQqCcjz.jpg" width="200">
        </div>
    """, unsafe_allow_html=True)

# Login screen
if not st.session_state.logged_in:
    login()
    st.stop()

# Initialize databases and models
@st.cache_resource
def load_resources():
    disease_db = DiseaseDatabase()
    treatment_db = TreatmentDatabase()
    image_processor = ImageProcessor()
    ml_model = CowDiseaseModel()
    db_manager = get_database_manager()
    return disease_db, treatment_db, image_processor, ml_model, db_manager



# Load resources
try:
    disease_db, treatment_db, image_processor, ml_model, db_manager = load_resources()
except Exception as e:
    st.error(f"Failed to initialize application resources: {str(e)}")
    st.stop()

# Main title
st.title("🐄 Pashu Raksha - Cow Disease Diagnosis")
st.markdown("Upload a photo of your cow to get AI-powered disease diagnosis and treatment recommendations")

# Sidebar for navigation
st.sidebar.title("Health Hub")
page = st.sidebar.selectbox("Choose a page", [
    "Diagnosis", 
    "Disease Database", 
    "Search Diseases", 
    "Prevention Guide",
    "Emergency Protocol",
    "Health Analytics",
    "Find Veterinarian",
    "Treatment Calculator",
    "Health Records"
])

if page == "Diagnosis":
    st.header("Upload Cow Image for Diagnosis")

    # Upload selection
    upload_option = st.radio("Upload Method:", ["Single Image", "Multiple Images"])

    if upload_option == "Single Image":
        uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
        uploaded_files = [uploaded_file] if uploaded_file else []
    else:
        uploaded_files = st.file_uploader("Choose multiple image files", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files and any(uploaded_files):
        valid_files = [f for f in uploaded_files if f is not None]
        all_predictions = []

        for idx, uploaded_file in enumerate(valid_files):
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Uploaded Image {idx + 1}", use_container_width=True)

                quality = image_processor.detect_image_quality(image)
                st.markdown("### 📷 Image Quality")
                st.info(f"Overall: {quality['overall_quality']}")
                if quality.get("issues"):
                    st.warning(f"Issues: {', '.join(quality['issues'])}")

                st.markdown(f"### 🧪 Analyzing Image {idx + 1}")
                processed = image_processor.preprocess_image(image)
                if processed is not None:
                    predictions = ml_model.predict(image)

                    if predictions:
                        all_predictions.extend(predictions)
                        for i, (disease_name, confidence) in enumerate(predictions[:3]):
                            st.markdown(f"### 🐮 Predicted Disease: **{disease_name}** (Confidence: {confidence:.1%})")

                            disease_info = disease_db.get_disease_info(disease_name)
                            treatment_info = treatment_db.get_treatment_info(disease_name)

                            if disease_info:
                                st.markdown("#### 🧬 Disease Information")
                                st.markdown(f"- **Description:** {disease_info['description']}")
                                st.markdown(f"- **Symptoms:** {disease_info['symptoms']}")
                                st.markdown(f"- **Causes:** {disease_info['causes']}")

                            if treatment_info:
                                st.markdown("#### 💊 Treatment Information")
                                st.markdown(f"- **Immediate Actions:** {treatment_info['immediate_actions']}")
                                st.markdown(f"- **Medications:** {treatment_info['medications']}")
                                st.markdown(f"- **Dosage:** {treatment_info['dosage']}")
                                st.markdown(f"- **Duration:** {treatment_info['duration']}")
                                st.markdown(f"- **Prevention:** {treatment_info['prevention']}")
                                st.info("⚠️ Always consult a veterinarian before applying treatment.")
                            else:
                                st.warning("🚫 No treatment info available.")
                            st.markdown("---")
                    else:
                        st.warning("No disease detected.")
                else:
                    st.error("Could not process image.")
            except Exception as e:
                st.error(f"Failed to process: {str(e)}")

        # Show summary for multiple images
        if len(valid_files) > 1 and all_predictions:
            st.header("📊 Summary Across All Images")
            count = {}
            confidence = {}

            for d, c in all_predictions:
                count[d] = count.get(d, 0) + 1
                confidence[d] = confidence.get(d, 0) + c

            for d in sorted(count, key=lambda x: (count[x], confidence[x]), reverse=True):
                avg_conf = confidence[d] / count[d]
                st.markdown(f"### 🔍 {d} (Detected in {count[d]} image(s), Avg Confidence: {avg_conf:.1%})")

                info = disease_db.get_disease_info(d)
                treat = treatment_db.get_treatment_info(d)

                if info:
                    st.markdown(f"- **Description:** {info['description']}")
                    st.markdown(f"- **Symptoms:** {info['symptoms']}")

                if treat:
                    st.markdown("#### 💊 Treatment Summary")
                    st.markdown(f"- **Medications:** {treat['medications']}")
                    st.markdown(f"- **Prevention:** {treat['prevention']}")


elif page == "Disease Database":
    st.header("📚 Cow Disease Database")
    
    # Get all diseases
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

elif page == "Search Diseases":
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

elif page == "Prevention Guide":
    st.header("🛡️ Disease Prevention Guide")
    
    # Prevention categories
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

elif page == "Emergency Protocol":
    st.header("🚨 Emergency Protocol Guide")
    
    st.warning("⚠️ This emergency guide is for **immediate first-response reference only**. Always consult a licensed veterinarian as soon as possible.")

    st.markdown("""
    This guide outlines how to identify and respond quickly to life-threatening or urgent conditions in cattle.
    """)
    
    emergencies = {
        "Severe Bloat": {
            "symptoms": [
                "⚠️ Severe abdominal distension (left side especially)",
                "😰 Difficulty breathing or groaning",
                "💥 Sudden collapse or restlessness"
            ],
            "immediate_actions": [
                "🚶 Keep animal **standing and walking** to release pressure",
                "🧪 Insert **stomach tube** if trained (to relieve gas buildup)",
                "📞 **Call veterinarian immediately** – life-threatening within minutes",
                "❌ **Do NOT** administer oral remedies unless directed",
                "👀 Monitor **breathing** and **abdominal girth** closely"
            ],
            "urgency": "🔴 CRITICAL – Act within **minutes**"
        },
        "Milk Fever Emergency": {
            "symptoms": [
                "🧊 Cold ears and limbs",
                "💤 Cow lying down and unable to stand",
                "💥 Muscle tremors or collapse after calving"
            ],
            "immediate_actions": [
                "🛏️ Provide **soft bedding** and keep animal **calm**",
                "📞 Contact **veterinarian for IV calcium** treatment",
                "🛑 Do **not** try to lift or force the cow to stand",
                "🌡️ Monitor **vital signs** if possible",
                "🧣 Keep cow **warm and protected** from drafts"
            ],
            "urgency": "🟠 URGENT – Act within **1–2 hours**"
        },
        "Severe Respiratory Distress": {
            "symptoms": [
                "😤 Open-mouth breathing or gasping",
                "🔵 Blue or purple gums (cyanosis)",
                "🫁 Labored or extremely rapid breathing"
            ],
            "immediate_actions": [
                "🌬️ Move animal to a **well-ventilated**, quiet area",
                "🔍 Remove any **visible obstructions** in nose or mouth",
                "📞 Call **veterinarian immediately**",
                "🧊 Apply **cool compresses** if fever is high",
                "🧘 Keep animal **calm** to reduce oxygen demand"
            ],
            "urgency": "🔴 CRITICAL – Act **immediately**"
        },
        "Prolapsed Uterus": {
            "symptoms": [
                "👀 Uterus visible **outside** the cow's body post-calving",
                "🩸 Possible bleeding or trauma",
                "😟 Cow may appear weak or distressed"
            ],
            "immediate_actions": [
                "🧼 Cover prolapsed tissue with **clean, moist cloth**",
                "🚫 Do **not attempt to replace** the uterus yourself",
                "📞 Contact **veterinarian immediately**",
                "🚷 Prevent contamination with dirt or manure",
                "🧍 Encourage the cow to **remain standing** if possible"
            ],
            "urgency": "🟠 URGENT – Act within **1 hour**"
        }
    }

    for emergency, details in emergencies.items():
        with st.expander(f"🚨 {emergency}"):
            st.subheader(details["urgency"])
            st.markdown("### 🧿 Symptoms to Look For")
            for symptom in details["symptoms"]:
                st.markdown(f"- {symptom}")
            st.markdown("### 🛠️ Immediate First-Aid Actions")
            for i, action in enumerate(details["immediate_actions"], start=1):
                st.markdown(f"{i}. {action}")
            st.markdown("---")

elif page == "Health Analytics":
    st.header("📊 Health Analytics Dashboard")
    
    st.info("Track your herd's health patterns and trends")
    
    # Mock data for demonstration - in real application, this would connect to farm management system
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Diagnoses This Month", "47", "12%")
    
    with col2:
        st.metric("Most Common Disease", "Mastitis", "35% of cases")
    
    with col3:
        st.metric("Prevention Success Rate", "78%", "5%")
    
    # Disease frequency chart
    st.subheader("📈 Disease Frequency Trends")
    
    import pandas as pd
    import random
    
    # Sample data for visualization
    diseases = ["Mastitis", "Lameness", "Respiratory Disease", "Ketosis", "Pink Eye"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    st.info("Health analytics requires connection to your farm management system or manual data entry to display real trends and statistics.")
    
    # Data input section
    st.subheader("📝 Manual Health Record Entry")
    
    with st.form("health_record_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cow_id = st.text_input("Cow ID/Tag Number")
            diagnosis_date = st.date_input("Diagnosis Date")
            diagnosed_disease = st.selectbox("Diagnosed Disease", 
                ["Mastitis", "Lameness", "Respiratory Disease", "Ketosis", "Pink Eye", "Other"])
        
        with col2:
            severity = st.selectbox("Severity Level", ["Mild", "Moderate", "Severe"])
            treatment_cost = st.number_input("Treatment Cost ($)", min_value=0.0, value=0.0)
            veterinarian = st.text_input("Veterinarian Name")
        
        notes = st.text_area("Additional Notes")
        
        submitted = st.form_submit_button("Add Health Record")
        
        if submitted and cow_id and diagnosed_disease:
            record_data = {
                'cow_id': cow_id,
                'diagnosis_date': diagnosis_date,
                'disease_name': diagnosed_disease,
                'severity': severity.lower(),
                'treatment_applied': f"Manual entry - {severity} {diagnosed_disease}",
                'total_cost': treatment_cost,
                'veterinarian': veterinarian,
                'notes': notes
            }
            
            if db_manager.add_health_record(record_data):
                st.success(f"Health record added for Cow {cow_id}")
            else:
                st.error("Failed to save health record to database")
    
    # Farm management system integration notice
    st.subheader("🔗 Integration Options")
    
    integration_options = [
        "**DairyComp 305** - Comprehensive dairy management",
        "**PCDART** - Production and health records",
        "**Herd Navigator** - Automated health monitoring", 
        "**CowManager** - Real-time health monitoring",
        "**Custom Database** - Your existing farm records"
    ]
    
    st.markdown("Connect with popular farm management systems:")
    for option in integration_options:
        st.markdown(f"• {option}")
    
    st.info("Contact your system administrator to set up data integration for real-time analytics.")

elif page == "Find Veterinarian":
    st.header("🏥 Find Veterinarian")
    
    st.markdown("Locate qualified veterinarians in your area for cow health services")
    
    # Location input
    col1, col2 = st.columns(2)
    
    with col1:
        location = st.text_input("Enter your location (City, State/ZIP)")
        service_type = st.selectbox("Service Type", [
            "General Veterinary Care",
            "Large Animal Specialist", 
            "Emergency Services",
            "Reproductive Services",
            "Nutrition Consultation",
            "Hoof Care Specialist"
        ])
    
    with col2:
        search_radius = st.slider("Search Radius (miles)", 5, 50, 25)
        availability = st.selectbox("Availability", [
            "Any time",
            "Emergency only",
            "Weekdays",
            "Weekends",
            "24/7 services"
        ])
    
    if st.button("Search Veterinarians") and location:
        st.info("Veterinarian search requires integration with veterinary directory services. Please contact local veterinary associations or use online directories.")
        
        # Sample veterinarian listings for demonstration
        st.subheader("📋 Veterinarian Directory")
        
        sample_vets = [
            {
                "name": "Dr. Sarah Johnson, DVM",
                "clinic": "Countryside Animal Hospital",
                "specialties": "Large Animal Medicine, Reproduction",
                "phone": "(555) 123-4567",
                "distance": "8.2 miles",
                "rating": "4.8/5",
                "emergency": True
            },
            {
                "name": "Dr. Michael Chen, DVM",
                "clinic": "Farm Animal Care Center",
                "specialties": "Dairy Health, Nutrition",
                "phone": "(555) 234-5678", 
                "distance": "12.5 miles",
                "rating": "4.9/5",
                "emergency": False
            },
            {
                "name": "Dr. Emily Rodriguez, DVM",
                "clinic": "Rural Veterinary Services",
                "specialties": "Emergency Care, Surgery",
                "phone": "(555) 345-6789",
                "distance": "15.1 miles", 
                "rating": "4.7/5",
                "emergency": True
            }
        ]
        
        for vet in sample_vets:
            with st.expander(f"🏥 {vet['name']} - {vet['clinic']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Specialties:** {vet['specialties']}")
                    st.markdown(f"**Phone:** {vet['phone']}")
                    st.markdown(f"**Distance:** {vet['distance']}")
                
                with col2:
                    st.markdown(f"**Rating:** {vet['rating']}")
                    if vet['emergency']:
                        st.success("✅ Emergency Services Available")
                    else:
                        st.info("Regular Hours Only")
                
                st.markdown("**Schedule Consultation:**")
                consultation_type = st.selectbox(f"Service for {vet['name']}", 
                    ["Regular Check-up", "Disease Diagnosis", "Emergency Visit", "Follow-up"], 
                    key=f"consult_{vet['name']}")
                
                if st.button(f"Contact {vet['name']}", key=f"contact_{vet['name']}"):
                    st.success(f"Contact information copied. Call {vet['phone']} to schedule.")

elif page == "Treatment Calculator":
    st.header("💊 Treatment Cost Calculator")
    
    st.markdown("Estimate treatment costs for common cow diseases (in Indian Rupees)")
    
    # Disease selection - costs converted to INR (approximate 1 USD = 83 INR)
    disease_costs = {
        "Mastitis": {
            "mild": {"medication": 2075, "labor": 1245, "supplies": 830},
            "moderate": {"medication": 4150, "labor": 2490, "supplies": 1660},
            "severe": {"medication": 8300, "labor": 4980, "supplies": 3320}
        },
        "Lameness": {
            "mild": {"medication": 1245, "labor": 2075, "supplies": 1245},
            "moderate": {"medication": 2905, "labor": 4150, "supplies": 2075},
            "severe": {"medication": 6225, "labor": 8300, "supplies": 4150}
        },
        "Bovine Respiratory Disease": {
            "mild": {"medication": 3320, "labor": 1660, "supplies": 1245},
            "moderate": {"medication": 6640, "labor": 3320, "supplies": 2490},
            "severe": {"medication": 12450, "labor": 6640, "supplies": 4980}
        },
        "Ketosis": {
            "mild": {"medication": 2490, "labor": 1245, "supplies": 830},
            "moderate": {"medication": 4980, "labor": 2490, "supplies": 1660},
            "severe": {"medication": 9960, "labor": 4980, "supplies": 3320}
        },
        "Pink Eye": {
            "mild": {"medication": 1660, "labor": 830, "supplies": 415},
            "moderate": {"medication": 2905, "labor": 1660, "supplies": 830},
            "severe": {"medication": 4980, "labor": 3320, "supplies": 1660}
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_disease = st.selectbox("Select Disease", list(disease_costs.keys()))
        severity_level = st.selectbox("Severity Level", ["mild", "moderate", "severe"])
        num_animals = st.number_input("Number of Animals Affected", min_value=1, max_value=100, value=1)
    
    with col2:
        vet_visit = st.checkbox("Veterinarian Visit Required", value=True)
        follow_up_visits = st.number_input("Follow-up Visits", min_value=0, max_value=5, value=1)
        prevention_program = st.checkbox("Add Prevention Program Cost")
    
    if selected_disease and severity_level:
        base_costs = disease_costs[selected_disease][severity_level]
        
        # Calculate total costs
        medication_cost = base_costs["medication"] * num_animals
        labor_cost = base_costs["labor"] * num_animals
        supplies_cost = base_costs["supplies"] * num_animals
        
        vet_cost = 6225 if vet_visit else 0  # ₹6,225 (75 USD * 83)
        follow_up_cost = follow_up_visits * 4150  # ₹4,150 per visit (50 USD * 83)
        prevention_cost = 16600 if prevention_program else 0  # ₹16,600 (200 USD * 83)
        
        total_cost = medication_cost + labor_cost + supplies_cost + vet_cost + follow_up_cost + prevention_cost
        
        st.subheader("💰 Cost Breakdown")
        
        cost_breakdown = {
            "Medications": medication_cost,
            "Labor": labor_cost,
            "Supplies": supplies_cost,
            "Veterinarian Visit": vet_cost,
            "Follow-up Visits": follow_up_cost,
            "Prevention Program": prevention_cost
        }
        
        for item, cost in cost_breakdown.items():
            if cost > 0:
                st.markdown(f"**{item}:** ₹{cost:,.2f}")
        
        st.markdown("---")
        st.markdown(f"### **Total Estimated Cost: ₹{total_cost:,.2f}**")
        
        # Cost per animal
        cost_per_animal = total_cost / num_animals
        st.markdown(f"**Cost per animal:** ₹{cost_per_animal:,.2f}")
        
        # Economic impact analysis
        st.subheader("📊 Economic Impact Analysis")
        
        # Estimated losses without treatment (converted to INR)
        loss_without_treatment = {
            "Mastitis": {"mild": 12450, "moderate": 33200, "severe": 66400},
            "Lameness": {"mild": 16600, "moderate": 41500, "severe": 83000},
            "Bovine Respiratory Disease": {"mild": 24900, "moderate": 49800, "severe": 99600},
            "Ketosis": {"mild": 20750, "moderate": 41500, "severe": 74700},
            "Pink Eye": {"mild": 8300, "moderate": 20750, "severe": 41500}
        }
        
        potential_loss = loss_without_treatment[selected_disease][severity_level] * num_animals
        savings = potential_loss - total_cost
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Treatment Cost", f"₹{total_cost:,.2f}")
        
        with col2:
            st.metric("Potential Loss Without Treatment", f"₹{potential_loss:,.2f}")
        
        with col3:
            st.metric("Estimated Savings", f"₹{savings:,.2f}", delta=f"₹{savings:,.2f}")
        
        if savings > 0:
            st.success(f"Treatment is economically beneficial. ROI: {(savings/total_cost)*100:.1f}%")
        else:
            st.warning("Treatment costs exceed potential losses for this severity level.")

elif page == "Health Records":
    st.header("📋 Health Records Management")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["View Records", "Search Records", "Statistics"])
    
    with tab1:
        st.subheader("Recent Health Records")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            cow_filter = st.text_input("Filter by Cow ID (optional)")
        with col2:
            limit = st.slider("Number of records to show", 10, 100, 50)
        
        # Get records from database
        records = db_manager.get_health_records(cow_id=cow_filter if cow_filter else None, limit=limit)
        
        if records:
            # Display records in a table
            df = pd.DataFrame(records)
            
            # Format the dataframe for better display
            display_df = df[['cow_id', 'diagnosis_date', 'disease_name', 'severity', 'total_cost', 'veterinarian']].copy()
            display_df.columns = ['Cow ID', 'Date', 'Disease', 'Severity', 'Cost (₹)', 'Veterinarian']
            
            # Format date and cost columns
            display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
            display_df['Cost (₹)'] = display_df['Cost (₹)'].fillna(0).apply(lambda x: f"₹{x:,.2f}" if x > 0 else "-")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Detailed view of selected record
            st.subheader("Detailed Record View")
            selected_cow = st.selectbox("Select Cow ID for detailed view", 
                                      options=[""] + list(df['cow_id'].unique()))
            
            if selected_cow:
                cow_records = df[df['cow_id'] == selected_cow].sort_values('diagnosis_date', ascending=False)
                
                for _, record in cow_records.iterrows():
                    with st.expander(f"{record['disease_name']} - {record['diagnosis_date'].strftime('%Y-%m-%d')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Disease:** {record['disease_name']}")
                            st.markdown(f"**Severity:** {record['severity']}")
                            st.markdown(f"**Date:** {record['diagnosis_date'].strftime('%Y-%m-%d %H:%M')}")
                            if record['confidence_score']:
                                st.markdown(f"**Confidence:** {record['confidence_score']:.1%}")
                        
                        with col2:
                            st.markdown(f"**Total Cost:** ₹{record['total_cost']:,.2f}" if record['total_cost'] else "Cost: Not specified")
                            st.markdown(f"**Veterinarian:** {record['veterinarian'] or 'Not specified'}")
                            if record['symptoms']:
                                st.markdown(f"**Symptoms:** {record['symptoms']}")
                        
                        if record['treatment_applied']:
                            st.markdown(f"**Treatment Applied:** {record['treatment_applied']}")
                        
                        if record['notes']:
                            st.markdown(f"**Notes:** {record['notes']}")
        else:
            st.info("No health records found. Start by adding records through the Health Analytics page or by saving diagnoses from the Diagnosis page.")
    
    with tab2:
        st.subheader("Search Health Records")
        
        search_term = st.text_input("Search by disease, cow ID, or notes:")
        
        if search_term:
            search_results = db_manager.search_records(search_term)
            
            if search_results:
                st.success(f"Found {len(search_results)} matching records")
                
                search_df = pd.DataFrame(search_results)
                display_search = search_df[['cow_id', 'diagnosis_date', 'disease_name', 'severity', 'total_cost']].copy()
                display_search.columns = ['Cow ID', 'Date', 'Disease', 'Severity', 'Cost (₹)']
                display_search['Date'] = pd.to_datetime(display_search['Date']).dt.strftime('%Y-%m-%d')
                display_search['Cost (₹)'] = display_search['Cost (₹)'].fillna(0).apply(lambda x: f"₹{x:,.2f}" if x > 0 else "-")
                
                st.dataframe(display_search, use_container_width=True)
            else:
                st.info("No records found matching your search criteria.")
    
    with tab3:
        st.subheader("Health Statistics")
        
        stats = db_manager.get_disease_statistics()
        
        if stats['total_records'] > 0:
            # Key metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", stats['total_records'])
            
            with col2:
                most_common = max(stats['disease_counts'].items(), key=lambda x: x[1]) if stats['disease_counts'] else ("None", 0)
                st.metric("Most Common Disease", most_common[0], f"{most_common[1]} cases")
            
            with col3:
                st.metric("Average Treatment Cost", f"₹{stats['average_cost']:,.2f}")
            
            # Disease distribution
            if stats['disease_counts']:
                st.subheader("Disease Distribution")
                disease_df = pd.DataFrame(list(stats['disease_counts'].items()), 
                                        columns=['Disease', 'Count'])
                st.bar_chart(disease_df.set_index('Disease'))
            
            # Recent trends
            st.subheader("Recent Activity")
            recent_records = db_manager.get_health_records(limit=10)
            if recent_records:
                recent_df = pd.DataFrame(recent_records)
                st.write("Last 10 diagnoses:")
                trend_display = recent_df[['diagnosis_date', 'cow_id', 'disease_name', 'severity']].copy()
                trend_display.columns = ['Date', 'Cow ID', 'Disease', 'Severity']
                trend_display['Date'] = pd.to_datetime(trend_display['Date']).dt.strftime('%Y-%m-%d %H:%M')
                st.dataframe(trend_display, use_container_width=True)
        else:
            st.info("No statistics available. Add some health records to see analytics.")
            
            # Sample data notice
            st.subheader("Getting Started")
            st.markdown("""
            To start using the health records system:
            1. Upload cow images in the **Diagnosis** page and save the results
            2. Manually add records in the **Health Analytics** page
            3. View and analyze your data here in **Health Records**
            
            The system will automatically track:
            - Disease patterns in your herd
            - Treatment costs and effectiveness
            - Historical health trends
            - Veterinarian contact information
            """)

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This application is for educational and preliminary assessment purposes only. Always consult with a qualified veterinarian for proper diagnosis and treatment of your livestock.")
