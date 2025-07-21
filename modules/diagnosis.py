import streamlit as st
from PIL import Image

def run(disease_db, treatment_db, image_processor, ml_model):
    st.header("Upload Cow Image for Diagnosis")

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
