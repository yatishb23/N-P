import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import shutil

# 1. Define classes and directories
DATA_DIR = "data/HAM10000"
METADATA_PATH = os.path.join(DATA_DIR, "HAM10000_metadata.csv")
MODEL_SAVE_PATH = "model.h5"

# The HAM10000 classes mapped to readable names
CLASSES = {
    'akiec': 'Actinic keratoses',
    'bcc': 'Basal cell carcinoma',
    'bkl': 'Benign keratosis-like lesions',
    'df': 'Dermatofibroma',
    'mel': 'Melanoma',
    'nv': 'Melanocytic nevi',
    'vasc': 'Vascular lesions'
}

def prepare_dataset():
    """
    Reads metadata, finds the actual image paths, and creates a consolidated 
    DataFrame for ImageDataGenerator.
    """
    print("Preparing dataset...")
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Metadata not found at {METADATA_PATH}. Did you extract the dataset?")

    df = pd.read_csv(METADATA_PATH)
    
    # Create image paths mapping
    image_paths = {}
    
    # HAM10000 provides images in part_1 and part_2
    part_1 = os.path.join(DATA_DIR, "HAM10000_images_part_1")
    part_2 = os.path.join(DATA_DIR, "HAM10000_images_part_2")
    
    for folder in [part_1, part_2]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith('.jpg'):
                    image_id = file.split('.')[0]
                    image_paths[image_id] = os.path.join(folder, file)

    df['path'] = df['image_id'].map(image_paths)
    df = df.dropna(subset=['path']) # Remove entries where image wasn't found
    df['cell_type'] = df['dx'].map(CLASSES)
    
    print(f"Total images found: {len(df)}")
    return df

def build_model(num_classes):
    print("Building MobileNetV2 Transfer Learning Model...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    # Compile
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

def main():
    try:
        df = prepare_dataset()
    except Exception as e:
        print(f"Error preparing dataset: {e}")
        return

    # Train/Val split
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['dx'])
    print(f"Training samples: {len(train_df)}, Validation samples: {len(val_df)}")

    # ImageDataGenerators with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)

    batch_size = 32 # Suitable for GTX 1650 4GB

    train_generator = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        x_col='path',
        y_col='cell_type',
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_dataframe(
        dataframe=val_df,
        x_col='path',
        y_col='cell_type',
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical'
    )

    num_classes = len(CLASSES)
    model = build_model(num_classes)
    
    # Save class indices to json for inference
    import json
    with open('class_indices.json', 'w') as f:
        json.dump(train_generator.class_indices, f)
    
    print("Starting training (this may take a while)...")
    epochs = 10 # Feel free to increase this for better accuracy
    
    model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator
    )

    print(f"Saving model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)
    print("Training complete! You can now run the Streamlit app.")

if __name__ == '__main__':
    # Warn user about missing GPU usage optimization
    print("Checking GPUs...")
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    main()
