import streamlit as st
import pandas as pd
from PIL import Image
import io
import os
from disease_database import DiseaseDatabase
from treatment_database import TreatmentDatabase
from image_processor import ImageProcessor
from ml_model import CowDiseaseModel

# Initialize databases and models
@st.cache_resource
def load_resources():
    disease_db = DiseaseDatabase()
    treatment_db = TreatmentDatabase()
    image_processor = ImageProcessor()
    ml_model = CowDiseaseModel()
    return disease_db, treatment_db, image_processor, ml_model

# Page configuration
st.set_page_config(
    page_title="Cow Disease Diagnosis System",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load resources
try:
    disease_db, treatment_db, image_processor, ml_model = load_resources()
except Exception as e:
    st.error(f"Failed to initialize application resources: {str(e)}")
    st.stop()

# Main title
st.title("🐄 Cow Disease Diagnosis System")
st.markdown("Upload a photo of your cow to get AI-powered disease diagnosis and treatment recommendations")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Diagnosis", "Disease Database", "Search Diseases"])

if page == "Diagnosis":
    st.header("Upload Cow Image for Diagnosis")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear photo of the cow showing any visible symptoms"
    )
    
    if uploaded_file is not None:
        try:
            # Display uploaded image
            image = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                st.subheader("Image Analysis")
                
                # Process image
                with st.spinner("Processing image..."):
                    processed_image = image_processor.preprocess_image(image)
                    
                if processed_image is not None:
                    st.success("✅ Image processed successfully")
                    
                    # Analyze with ML model
                    with st.spinner("Analyzing for diseases..."):
                        predictions = ml_model.predict(processed_image)
                    
                    if predictions:
                        st.subheader("🔍 Diagnosis Results")
                        
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
                        st.warning("No diseases detected. The cow appears healthy, but consult a veterinarian if you notice any concerning symptoms.")
                else:
                    st.error("Failed to process the uploaded image. Please try with a different image.")
                    
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            st.info("Please ensure you've uploaded a valid image file (PNG, JPG, or JPEG)")

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

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This application is for educational and preliminary assessment purposes only. Always consult with a qualified veterinarian for proper diagnosis and treatment of your livestock.")
