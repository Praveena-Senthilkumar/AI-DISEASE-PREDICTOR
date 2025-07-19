import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

# === STEP 1: Configuration ===
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25  # You can increase this for better accuracy
DATASET_PATH = "dataset"  # Change if your dataset folder is named differently
MODEL_OUTPUT_PATH = "model/trained_model.h5"

# === STEP 2: Data Augmentation and Loading ===
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# === STEP 3: MobileNetV2 Base Model ===
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base

# === STEP 4: Add Classification Head ===
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# === STEP 5: Compile Model ===
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# === STEP 6: Train Model ===
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# === STEP 7: Save Model ===
os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
model.save(MODEL_OUTPUT_PATH)

print(f"✅ Model trained and saved to {MODEL_OUTPUT_PATH}")
print(train_generator.class_indices)
