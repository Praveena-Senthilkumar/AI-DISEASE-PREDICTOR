import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load trained model
MODEL_PATH = os.path.join("cow_disease_model", "model", "trained_model.h5")  # Updated to match your path
model = load_model(MODEL_PATH)

# Classes used during training
CLASS_NAMES = [
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
# Same order used in dataset folders

def preprocess_image(img_pil, target_size=(224, 224)):
    img_resized = img_pil.resize(target_size)
    img_array = image.img_to_array(img_resized)
    img_array = img_array / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Batch dim
    return img_array

def predict_disease_from_pil(img_pil):
    img_array = preprocess_image(img_pil)
    preds = model.predict(img_array)[0]
    top_indices = preds.argsort()[-3:][::-1]
    return [(CLASS_NAMES[i], float(preds[i])) for i in top_indices]
