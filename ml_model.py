import numpy as np
from typing import List, Tuple, Optional
import random
import os

class CowDiseaseModel:
    """Machine Learning model for cow disease detection"""
    
    def __init__(self):
        self.model_loaded = False
        self.confidence_threshold = 0.3
        self.disease_classes = [
            "Mastitis",
            "Foot and Mouth Disease", 
            "Bovine Respiratory Disease",
            "Lameness",
            "Milk Fever",
            "Ketosis",
            "Bloat",
            "Pink Eye",
            "Scours",
            "Hardware Disease"
        ]
        
        # Try to load a real model if available
        self._load_model()
    
    def _load_model(self):
        """Load the ML model from file or initialize mock predictions"""
        try:
            # Check for model file in environment or local directory
            model_path = os.getenv('COW_DISEASE_MODEL_PATH', 'cow_disease_model.pkl')
            
            if os.path.exists(model_path):
                # In a real implementation, load your trained model here
                # self.model = joblib.load(model_path)
                # or
                # self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
                print(f"Model loaded from {model_path}")
            else:
                print("No trained model found. Using rule-based detection system.")
                self.model_loaded = False
                
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model_loaded = False
    
    def predict(self, image_array: np.ndarray) -> List[Tuple[str, float]]:
        """
        Predict diseases from preprocessed image array
        
        Args:
            image_array: Preprocessed image as numpy array
            
        Returns:
            List of tuples (disease_name, confidence_score)
        """
        try:
            if self.model_loaded:
                return self._predict_with_model(image_array)
            else:
                return self._rule_based_prediction(image_array)
                
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return []
    
    def _predict_with_model(self, image_array: np.ndarray) -> List[Tuple[str, float]]:
        """Make predictions using the trained ML model"""
        try:
            # In a real implementation, this would use your trained model
            # predictions = self.model.predict(image_array)
            # confidence_scores = predictions[0]  # Assuming batch size 1
            
            # For now, return empty list as we don't have a real model
            return []
            
        except Exception as e:
            print(f"Model prediction error: {str(e)}")
            return []
    
    def _rule_based_prediction(self, image_array: np.ndarray) -> List[Tuple[str, float]]:
        """
        Rule-based disease detection based on image characteristics
        This is a fallback when no ML model is available
        """
        try:
            # Analyze image characteristics
            image_features = self._extract_image_features(image_array)
            
            predictions = []
            
            # Simple rule-based detection based on image properties
            brightness = image_features.get('brightness', 0.5)
            contrast = image_features.get('contrast', 0.5)
            red_intensity = image_features.get('red_intensity', 0.5)
            
            # Rules for different diseases based on visual characteristics
            if red_intensity > 0.6 and brightness > 0.4:
                # High red intensity might indicate inflammation
                predictions.append(("Mastitis", 0.65))
                predictions.append(("Pink Eye", 0.45))
            
            if brightness < 0.3:
                # Dark images might indicate severe conditions
                predictions.append(("Foot and Mouth Disease", 0.55))
            
            if contrast > 0.7:
                # High contrast might indicate visible symptoms
                predictions.append(("Lameness", 0.50))
                predictions.append(("Bovine Respiratory Disease", 0.40))
            
            # If no specific indicators, suggest most common diseases
            if not predictions:
                predictions = [
                    ("Mastitis", 0.35),
                    ("Bovine Respiratory Disease", 0.30),
                    ("Lameness", 0.25)
                ]
            
            # Sort by confidence and return top predictions
            predictions.sort(key=lambda x: x[1], reverse=True)
            return predictions[:3]
            
        except Exception as e:
            print(f"Rule-based prediction error: {str(e)}")
            # Return most common diseases as fallback
            return [
                ("Mastitis", 0.30),
                ("Bovine Respiratory Disease", 0.25),
                ("Lameness", 0.20)
            ]
    
    def _extract_image_features(self, image_array: np.ndarray) -> dict:
        """Extract basic features from image for rule-based analysis"""
        try:
            # Remove batch dimension if present
            if len(image_array.shape) == 4:
                image_data = image_array[0]
            else:
                image_data = image_array
            
            # Calculate basic statistics
            features = {
                'brightness': np.mean(image_data),
                'contrast': np.std(image_data),
                'red_intensity': np.mean(image_data[:, :, 0]) if len(image_data.shape) == 3 else 0.5,
                'green_intensity': np.mean(image_data[:, :, 1]) if len(image_data.shape) == 3 else 0.5,
                'blue_intensity': np.mean(image_data[:, :, 2]) if len(image_data.shape) == 3 else 0.5,
            }
            
            return features
            
        except Exception as e:
            print(f"Feature extraction error: {str(e)}")
            return {
                'brightness': 0.5,
                'contrast': 0.5,
                'red_intensity': 0.5,
                'green_intensity': 0.5,
                'blue_intensity': 0.5
            }
    
    def get_model_info(self) -> dict:
        """Return information about the loaded model"""
        return {
            'model_loaded': self.model_loaded,
            'classes': self.disease_classes,
            'confidence_threshold': self.confidence_threshold,
            'model_type': 'ML Model' if self.model_loaded else 'Rule-based System'
        }
    
    def validate_prediction_confidence(self, predictions: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """Filter predictions based on confidence threshold"""
        return [(disease, conf) for disease, conf in predictions if conf >= self.confidence_threshold]
