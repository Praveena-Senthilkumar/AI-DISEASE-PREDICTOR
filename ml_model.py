import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

class CowDiseaseModel:
    def __init__(self):
        # Update model path relative to your project
        self.model_path = os.path.join("cow_disease_model", "model", "trained_model.h5")
        self.class_names = [
            'Actinomycosis',
            'Anthrax',
            'BovinePapillomatosis',
            'Brucellosis',
            'Footrot',
            'LumpySkinDisease',
            'Mastitis',
            'Pinkeye',
            'Ringworm',
            'TickInfestation'
        ]

        self.confidence_threshold = 0.3
        self.model_loaded = False
        self._load_model()

    def _load_model(self):
        try:
            self.model = load_model(self.model_path)
            self.model_loaded = True
            print(f"✅ Model loaded successfully from: {self.model_path}")
        except Exception as e:
            print(f"❌ Failed to load model: {str(e)}")
            self.model_loaded = False

    def preprocess_image(self, img_pil: Image.Image, target_size=(224, 224)) -> np.ndarray:
        try:
            img_resized = img_pil.resize(target_size)
            img_array = image.img_to_array(img_resized)
            img_array = img_array / 255.0  # Normalize
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            return img_array.astype(np.float32)
        except Exception as e:
            print(f"❌ Image preprocessing error: {e}")
            return None

    def predict(self, img_pil: Image.Image):
        if not self.model_loaded:
            print("❌ Model is not loaded.")
            return []

        preprocessed = self.preprocess_image(img_pil)
        if preprocessed is None:
            return []

        try:
            preds = self.model.predict(preprocessed)[0]
            top_indices = preds.argsort()[-3:][::-1]
            results = [(self.class_names[i], float(preds[i])) for i in top_indices]
            return self.validate_prediction_confidence(results)
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            return []

    def validate_prediction_confidence(self, predictions):
        """Return only predictions above confidence threshold"""
        return [(disease, conf) for disease, conf in predictions if conf >= self.confidence_threshold]

    def get_model_info(self):
        return {
            'model_loaded': self.model_loaded,
            'classes': self.class_names,
            'confidence_threshold': self.confidence_threshold,
            'model_type': 'Custom Keras CNN'
        }

#venv\Scripts\activate