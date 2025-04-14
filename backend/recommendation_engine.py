import numpy as np
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import tensorflow as tf
import json
import os

# Load affiliate links data (static demonstration)
AFFILIATE_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/affiliate_links.json")
if os.path.exists(AFFILIATE_DATA_PATH):
    with open(AFFILIATE_DATA_PATH, "r") as f:
        AFFILIATE_LINKS = json.load(f)
else:
    AFFILIATE_LINKS = {
        "top": "https://www.example.com/top",
        "bottom": "https://www.example.com/bottom",
        "dress": "https://www.example.com/dress",
        "outerwear": "https://www.example.com/outerwear"
    }

# Path to the saved model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/stylist_model.h5")
try:
    stylist_model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Warning: Model could not be loaded, using dummy predictions. ({e})")
    stylist_model = None

def analyze_image(image_stream: BytesIO) -> dict:
    image_stream.seek(0)
    color_thief = ColorThief(image_stream)
    dominant_color = color_thief.get_color(quality=1)
    hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)
    
    image_stream.seek(0)
    image = Image.open(image_stream)
    width, height = image.size

    return {
        "dominant_color": dominant_color,
        "hex_color": hex_color,
        "width": width,
        "height": height
    }

def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_style_features(image: Image.Image) -> dict:
    img_array = preprocess_image(image)
    classes = ["top", "bottom", "dress", "outerwear"]
    if stylist_model:
        prediction = stylist_model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_item = classes[predicted_index]
        confidence = float(prediction[predicted_index])
    else:
        brightness = np.mean(np.array(image))
        predicted_item = "top" if brightness > 150 else "outerwear"
        confidence = 0.75

    return {
        "predicted_item": predicted_item,
        "confidence": confidence,
        "affiliate_link": AFFILIATE_LINKS.get(predicted_item, "")
    }

def recommend_style(image_stream: BytesIO, analysis_results: dict) -> dict:
    image_stream.seek(0)
    image = Image.open(image_stream)
    style_prediction = predict_style_features(image)
    
    recommendation_details = {
        "suggested_item": style_prediction["predicted_item"],
        "description": (
            f"Based on your image analysis, we recommend a '{style_prediction['predicted_item']}' "
            f"that complements your dominant color {analysis_results['hex_color']}."
        ),
        "affiliate_link": style_prediction["affiliate_link"]
    }
    return recommendation_details
