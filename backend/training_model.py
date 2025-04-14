# import os
# import json
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.optimizers import Adam
# from sklearn.model_selection import train_test_split

# from PIL import Image

# # Global parameters
# IMAGE_SIZE = (224, 224)
# BATCH_SIZE = 32
# EPOCHS = 10
# NUM_CLASSES = 4  # classes: top, bottom, dress, outerwear

# # Mapping categories from annotations to our standardized classes.
# # Adjust or extend these mappings based on the dataset annotations.
# CATEGORY_MAPPING = {
#     "sling dress": "dress",
#     "dress": "dress",
#     "top": "top",
#     "blouse": "top",
#     "vest": "top",
#     "trouser": "bottom",
#     "skirt": "bottom",
#     "outerwear": "outerwear",
#     "jacket": "outerwear",
#     "coat": "outerwear",
#     # Add more mappings as needed...
# }

# # Directories (DeepFashion2 folder is at the root level)
# DATA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deepfashion2")
# IMAGE_DIR = os.path.join(DATA_ROOT, "image")
# ANNOT_DIR = os.path.join(DATA_ROOT, "annos")

# def load_dataset():
#     """
#     Loads images and their corresponding labels (extracted from JSON annotations) 
#     from the DeepFashion2 dataset. Returns image arrays and one-hot encoded labels.
#     """
#     file_names = sorted(os.listdir(IMAGE_DIR))
#     X = []
#     y = []
#     label_to_index = {"top": 0, "bottom": 1, "dress": 2, "outerwear": 3}
    
#     for file_name in file_names:
#         image_path = os.path.join(IMAGE_DIR, file_name)
#         annot_path = os.path.join(ANNOT_DIR, os.path.splitext(file_name)[0] + ".json")
        
#         if not os.path.exists(annot_path):
#             continue  # Skip if annotation file is missing
        
#         # Load and preprocess image
#         try:
#             img = Image.open(image_path).convert("RGB")
#             img = img.resize(IMAGE_SIZE)
#             img_array = np.array(img) / 255.0
#         except Exception as e:
#             print(f"Error loading image {image_path}: {e}")
#             continue
        
#         # Load JSON annotation and extract category
#         try:
#             with open(annot_path, "r") as f:
#                 annotation = json.load(f)
#             # Prefer item1 if it exists; otherwise, use item2.
#             if "item1" in annotation:
#                 cat = annotation["item1"].get("category_name", "").lower()
#             elif "item2" in annotation:
#                 cat = annotation["item2"].get("category_name", "").lower()
#             else:
#                 cat = ""
#             mapped_cat = CATEGORY_MAPPING.get(cat, None)
#             if mapped_cat is None:
#                 continue  # Skip if category not mapped
#             label_index = label_to_index[mapped_cat]
#         except Exception as e:
#             print(f"Error processing annotation {annot_path}: {e}")
#             continue
        
#         X.append(img_array)
#         y.append(label_index)
    
#     if not X:
#         raise ValueError("No data loaded. Please check your dataset paths and annotations.")
    
#     X = np.array(X)
#     y = tf.keras.utils.to_categorical(np.array(y), num_classes=NUM_CLASSES)
#     return X, y

# def create_transfer_model():
#     base_model = MobileNetV2(
#         weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
#     )
#     base_model.trainable = False
#     model = Sequential([
#         base_model,
#         GlobalAveragePooling2D(),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(NUM_CLASSES, activation='softmax')
#     ])
#     model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
#     return model

# def main():
#     print("Loading dataset...")
#     X, y = load_dataset()
#     print(f"Loaded {len(X)} samples.")

#     # Split into training and validation sets (80/20 split)
#     X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     # Create and summarize the model
#     model = create_transfer_model()
#     model.summary()
    
#     # Train the model
#     history = model.fit(
#         X_train, y_train,
#         validation_data=(X_val, y_val),
#         epochs=EPOCHS,
#         batch_size=BATCH_SIZE
#     )
    
#     # Save the trained model for inference
#     model_dir = os.path.join(os.path.dirname(__file__), "models")
#     os.makedirs(model_dir, exist_ok=True)
#     model.save(os.path.join(model_dir, "stylist_model.h5"))
#     print("Model saved successfully!")

# if __name__ == "__main__":
#     main()



import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from PIL import Image

# Global parameters
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 4  # classes: top, bottom, dress, outerwear

# Mapping categories from annotations to our standardized classes.
# Adjust or extend these mappings based on the dataset annotations.
CATEGORY_MAPPING = {
    "sling dress": "dress",
    "dress": "dress",
    "top": "top",
    "blouse": "top",
    "vest": "top",
    "trouser": "bottom",
    "skirt": "bottom",
    "outerwear": "outerwear",
    "jacket": "outerwear",
    "coat": "outerwear",
    # Add more mappings as needed...
}

# Directories (Assuming deepfashion2 is at the root level)
# Adjust this if your deepfashion2 folder is elsewhere
DATA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deepfashion2")
IMAGE_DIR = os.path.join(DATA_ROOT, "image")
ANNOT_DIR = os.path.join(DATA_ROOT, "annos")

def load_dataset(max_samples=None):
    """
    Loads images and corresponding labels from DeepFashion2.
    Optionally, limit the number of samples loaded (useful for debugging with large datasets).

    Returns:
        X: numpy array of images
        y: one-hot encoded labels
    """
    print("DATA_ROOT is set to:", DATA_ROOT)
    print("Looking for images in:", IMAGE_DIR)
    print("Looking for annotations in:", ANNOT_DIR)

    file_names = sorted(os.listdir(IMAGE_DIR))
    print(f"Found {len(file_names)} image files. Sample filenames: {file_names[:5]}")

    X = []
    y = []
    label_to_index = {"top": 0, "bottom": 1, "dress": 2, "outerwear": 3}
    count = 0

    for file_name in file_names:
        if max_samples is not None and count >= max_samples:
            break

        image_path = os.path.join(IMAGE_DIR, file_name)
        # Create the annotation file name assuming extension changes to .json
        annot_path = os.path.join(ANNOT_DIR, os.path.splitext(file_name)[0] + ".json")
        
        if not os.path.exists(annot_path):
            print(f"[WARNING] No annotation file for image {file_name}. Expected at: {annot_path}")
            continue

        # Load and preprocess image
        try:
            img = Image.open(image_path).convert("RGB")
            img = img.resize(IMAGE_SIZE)
            img_array = np.array(img) / 255.0
        except Exception as e:
            print(f"[ERROR] Could not load image {image_path}: {e}")
            continue

        # Load JSON annotation and extract category
        try:
            with open(annot_path, "r") as f:
                annotation = json.load(f)
            # Check if annotation contains either "item1" or "item2"
            if "item1" in annotation:
                cat = annotation["item1"].get("category_name", "").lower()
            elif "item2" in annotation:
                cat = annotation["item2"].get("category_name", "").lower()
            else:
                print(f"[WARNING] No 'item1' or 'item2' key found in annotation {annot_path}.")
                continue

            mapped_cat = CATEGORY_MAPPING.get(cat, None)
            if mapped_cat is None:
                print(f"[WARNING] Unmapped category '{cat}' in {annot_path}. Skipping file.")
                continue

            label_index = label_to_index[mapped_cat]
        except Exception as e:
            print(f"[ERROR] Could not process annotation {annot_path}: {e}")
            continue

        # Debug: Show first few processed filenames and labels
        if count < 5:
            print(f"[DEBUG] Processed file: {file_name} -> Category: {cat} mapped to {mapped_cat}")

        X.append(img_array)
        y.append(label_index)
        count += 1

    if not X:
        raise ValueError("No data loaded. Please check your dataset paths and annotations.")

    X = np.array(X)
    y = tf.keras.utils.to_categorical(np.array(y), num_classes=NUM_CLASSES)
    return X, y

def create_transfer_model():
    base_model = MobileNetV2(
        weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    )
    base_model.trainable = False
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(NUM_CLASSES, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    print("Loading dataset...")
    # For testing purposes, you can set max_samples to a small number (e.g., 50) to check if loading works.
    X, y = load_dataset(max_samples=50)  # Remove or set to None to load the full dataset.
    print(f"Loaded {len(X)} samples.")

    # Split into training and validation sets (80/20 split)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and summarize the model
    model = create_transfer_model()
    model.summary()

    # Train the model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )

    # Save the trained model for inference
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    model_save_path = os.path.join(model_dir, "stylist_model.h5")
    model.save(model_save_path)
    print("Model saved successfully at:", model_save_path)

if __name__ == "__main__":
    main()
