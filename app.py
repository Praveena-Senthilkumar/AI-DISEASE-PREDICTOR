import streamlit as st
import pandas as pd
from PIL import Image
import io
import os
from datetime import datetime, date
from disease_database import DiseaseDatabase
from treatment_database import TreatmentDatabase
from image_processor import ImageProcessor
from ml_model import CowDiseaseModel
from database import get_database_manager

# Initialize databases and models
@st.cache_resource
def load_resources():
    disease_db = DiseaseDatabase()
    treatment_db = TreatmentDatabase()
    image_processor = ImageProcessor()
    ml_model = CowDiseaseModel()
    db_manager = get_database_manager()
    return disease_db, treatment_db, image_processor, ml_model, db_manager

# Page configuration
st.set_page_config(
    page_title="Cow Disease Diagnosis System",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load resources
try:
    disease_db, treatment_db, image_processor, ml_model, db_manager = load_resources()
except Exception as e:
    st.error(f"Failed to initialize application resources: {str(e)}")
    st.stop()

# Main title
st.title("🐄 Cow Disease Diagnosis System")
st.markdown("Upload a photo of your cow to get AI-powered disease diagnosis and treatment recommendations")

# Sidebar for navigation
st.sidebar.title("Navigation")
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
    
    # Upload options
    upload_option = st.radio("Upload Method:", ["Single Image", "Multiple Images"])
    
    if upload_option == "Single Image":
        # Single file upload
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of the cow showing any visible symptoms"
        )
        uploaded_files = [uploaded_file] if uploaded_file else []
    else:
        # Multiple file upload
        uploaded_files = st.file_uploader(
            "Choose multiple image files",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Upload multiple photos for comprehensive analysis"
        )
    
    if uploaded_files and any(uploaded_files):
        # Filter out None values
        valid_files = [f for f in uploaded_files if f is not None]
        
        if valid_files:
            st.success(f"Processing {len(valid_files)} image(s)...")
            
            # Process each image
            all_predictions = []
            
            for idx, uploaded_file in enumerate(valid_files):
                try:
                    # Display uploaded image
                    image = Image.open(uploaded_file)
                    
                    st.markdown(f"### Image {idx + 1}: {uploaded_file.name}")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.image(image, caption=f"Uploaded Image {idx + 1}", use_container_width=True)
                        
                        # Image quality assessment
                        quality_info = image_processor.detect_image_quality(image)
                        st.markdown("**Image Quality Assessment:**")
                        if quality_info.get('overall_quality') == 'good':
                            st.success("✅ Good image quality")
                        elif quality_info.get('overall_quality') == 'fair':
                            st.warning("⚠️ Fair image quality")
                            if quality_info.get('issues'):
                                st.write(f"Issues: {', '.join(quality_info['issues'])}")
                        else:
                            st.error("❌ Poor image quality")
                            if quality_info.get('issues'):
                                st.write(f"Issues: {', '.join(quality_info['issues'])}")
                    
                    with col2:
                        st.subheader(f"Analysis for Image {idx + 1}")
                        
                        # Process image
                        with st.spinner("Processing image..."):
                            processed_image = image_processor.preprocess_image(image)
                            
                        if processed_image is not None:
                            st.success("✅ Image processed successfully")
                            
                            # Extract features for display
                            features = image_processor.extract_features(image)
                            with st.expander("📊 Image Features"):
                                st.write(f"Brightness: {features.get('brightness', 0):.2f}")
                                st.write(f"Contrast: {features.get('contrast', 0):.2f}")
                                st.write(f"Size: {features.get('size', 'Unknown')}")
                            
                            # Analyze with ML model
                            with st.spinner("Analyzing for diseases..."):
                                predictions = ml_model.predict(processed_image)
                            
                            if predictions:
                                all_predictions.extend(predictions)
                                st.subheader(f"🔍 Diagnosis Results for Image {idx + 1}")
                                
                                for i, (disease_name, confidence) in enumerate(predictions[:3]):
                                    with st.expander(f"{disease_name} (Confidence: {confidence:.1%})", expanded=(i==0)):
                                        disease_info = disease_db.get_disease_info(disease_name)
                                        treatment_info = treatment_db.get_treatment_info(disease_name)
                                        
                                        if disease_info:
                                            st.markdown(f"**Description:** {disease_info['description']}")
                                            st.markdown(f"**Symptoms:** {disease_info['symptoms']}")
                                            st.markdown(f"**Causes:** {disease_info['causes']}")
                                            
                                            if treatment_info:
                                                st.markdown("### 🏥 Treatment Recommendations")
                                                st.markdown(f"**Immediate Actions:** {treatment_info['immediate_actions']}")
                                                st.markdown(f"**Medications:** {treatment_info['medications']}")
                                                st.markdown(f"**Dosage:** {treatment_info['dosage']}")
                                                st.markdown(f"**Duration:** {treatment_info['duration']}")
                                                st.markdown(f"**Prevention:** {treatment_info['prevention']}")
                                                
                                                # Warning for veterinary consultation
                                                st.warning("⚠️ Always consult with a qualified veterinarian before administering any treatment.")
                                        else:
                                            st.error(f"Disease information not found for {disease_name}")
                            else:
                                st.warning(f"No diseases detected in image {idx + 1}.")
                        else:
                            st.error(f"Failed to process image {idx + 1}. Please try with a different image.")
                    
                    st.markdown("---")
                            
                except Exception as e:
                    st.error(f"Error processing image {idx + 1}: {str(e)}")
                    continue
            
            # Aggregate results for multiple images
            if len(valid_files) > 1 and all_predictions:
                st.header("📋 Comprehensive Analysis Summary")
                
                # Aggregate predictions by counting occurrences
                disease_counts = {}
                confidence_sums = {}
                
                for disease, confidence in all_predictions:
                    if disease in disease_counts:
                        disease_counts[disease] += 1
                        confidence_sums[disease] += confidence
                    else:
                        disease_counts[disease] = 1
                        confidence_sums[disease] = confidence
                
                # Calculate average confidence and sort by frequency
                aggregated_results = []
                for disease in disease_counts:
                    avg_confidence = confidence_sums[disease] / disease_counts[disease]
                    frequency = disease_counts[disease]
                    aggregated_results.append((disease, avg_confidence, frequency))
                
                aggregated_results.sort(key=lambda x: (x[2], x[1]), reverse=True)
                
                st.subheader("🎯 Most Likely Diagnoses Across All Images")
                
                for disease, avg_conf, freq in aggregated_results[:5]:
                    with st.expander(f"{disease} (Detected in {freq}/{len(valid_files)} images, Avg Confidence: {avg_conf:.1%})"):
                        disease_info = disease_db.get_disease_info(disease)
                        treatment_info = treatment_db.get_treatment_info(disease)
                        
                        if disease_info:
                            col1, col2 = st.columns([1, 1])
                            
                            with col1:
                                st.markdown("### Disease Information")
                                st.markdown(f"**Description:** {disease_info['description']}")
                                st.markdown(f"**Symptoms:** {disease_info['symptoms']}")
                                st.markdown(f"**Severity:** {disease_info.get('severity', 'Unknown')}")
                            
                            with col2:
                                if treatment_info:
                                    st.markdown("### Treatment Protocol")
                                    st.markdown(f"**Immediate Actions:** {treatment_info['immediate_actions']}")
                                    st.markdown(f"**Medications:** {treatment_info['medications']}")
                                    st.markdown(f"**Prevention:** {treatment_info['prevention']}")
                                    
                st.info(f"Analysis based on {len(valid_files)} images. Multiple image analysis provides more reliable diagnosis.")
        else:
            st.info("Please upload at least one valid image file.")

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
    
    st.warning("⚠️ This guide is for immediate reference only. Always contact a veterinarian for emergencies.")
    
    # Emergency situations
    emergencies = {
        "Severe Bloat": {
            "symptoms": "Severe abdominal distension, difficulty breathing, collapse",
            "immediate_actions": [
                "Keep animal standing and moving",
                "Insert stomach tube if trained",
                "Contact veterinarian immediately",
                "Do NOT give oral medications",
                "Monitor breathing closely"
            ],
            "urgency": "CRITICAL - Act within minutes"
        },
        "Milk Fever Emergency": {
            "symptoms": "Unable to stand, muscle tremors, cold extremities",
            "immediate_actions": [
                "Keep cow calm and warm",
                "Contact veterinarian for IV calcium",
                "Do not attempt to force standing",
                "Provide soft bedding",
                "Monitor for complications"
            ],
            "urgency": "URGENT - Act within 1-2 hours"
        },
        "Severe Respiratory Distress": {
            "symptoms": "Open-mouth breathing, blue gums, extreme difficulty breathing",
            "immediate_actions": [
                "Move to well-ventilated area",
                "Remove any obstructions from airway",
                "Contact veterinarian immediately",
                "Monitor temperature",
                "Keep animal calm"
            ],
            "urgency": "CRITICAL - Act immediately"
        },
        "Prolapsed Uterus": {
            "symptoms": "Uterus visible outside body after calving",
            "immediate_actions": [
                "Cover with clean, moist cloth",
                "Prevent further contamination",
                "Contact veterinarian immediately",
                "Do NOT attempt to replace yourself",
                "Keep cow standing if possible"
            ],
            "urgency": "URGENT - Act within 1 hour"
        }
    }
    
    for emergency, details in emergencies.items():
        with st.expander(f"🚨 {emergency}"):
            st.error(f"**Urgency Level:** {details['urgency']}")
            st.markdown(f"**Symptoms:** {details['symptoms']}")
            st.markdown("**Immediate Actions:**")
            for action in details['immediate_actions']:
                st.markdown(f"1. {action}")

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
