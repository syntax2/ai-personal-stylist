# backend/recommendation_engine.py
import numpy as np
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import tensorflow as tf
import json
import os

# Load affiliate links data (for demonstration, we use static JSON data)
AFFILIATE_DATA_PATH = "../data/affiliate_links.json"
if os.path.exists(AFFILIATE_DATA_PATH):
    with open(AFFILIATE_DATA_PATH, "r") as f:
        AFFILIATE_LINKS = json.load(f)
else:
    AFFILIATE_LINKS = {
        "shirt": "https://www.example.com/shirt",
        "jacket": "https://www.example.com/jacket",
        "trousers": "https://www.example.com/trousers"
    }

# Model path for our stylist recommendation model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/stylist_model.h5")

# Attempt to load model. If not present, use None and fall back to rule-based logic.
try:
    stylist_model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Warning: Model could not be loaded, using dummy predictions. ({e})")
    stylist_model = None

def analyze_image(image_stream: BytesIO) -> dict:
    """
    Analyzes the image to extract dominant color and basic metrics.
    """
    # Use ColorThief to get the dominant color
    image_stream.seek(0)
    color_thief = ColorThief(image_stream)
    dominant_color = color_thief.get_color(quality=1)
    hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color)
    
    # Optional: use Pillow to load the image for further analysis (e.g. size, brightness)
    image_stream.seek(0)
    image = Image.open(image_stream)
    width, height = image.size

    # Return basic analysis results
    return {
        "dominant_color": dominant_color,
        "hex_color": hex_color,
        "width": width,
        "height": height
    }

def predict_style_features(image: Image.Image) -> dict:
    """
    Runs a prediction on the pre-trained stylist model using the user image.
    This function assumes you have a model trained that takes a resized image input.
    """
    # Resize and preprocess the image for the model input (assuming 224x224)
    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0  # normalize pixels
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension

    if stylist_model:
        prediction = stylist_model.predict(img_array)[0]
        # For demonstration, assume prediction outputs probabilities for various clothing items:
        # e.g., [shirt_prob, jacket_prob, trousers_prob]
        items = ["shirt", "jacket", "trousers"]
        predicted_index = np.argmax(prediction)
        predicted_item = items[predicted_index]
        confidence = float(prediction[predicted_index])
    else:
        # Fall back to rule-based dummy logic based on dominant color brightness
        brightness = np.mean(np.array(image))
        if brightness > 150:
            predicted_item = "shirt"
            confidence = 0.8
        else:
            predicted_item = "jacket"
            confidence = 0.7

    return {
        "predicted_item": predicted_item,
        "confidence": confidence,
        "affiliate_link": AFFILIATE_LINKS.get(predicted_item, "")
    }

def recommend_style(image_stream: BytesIO, analysis_results: dict) -> dict:
    """
    Combines image analysis with a style recommendation.
    """
    image_stream.seek(0)
    image = Image.open(image_stream)
    style_prediction = predict_style_features(image)
    
    # You can add more recommendation logic, e.g., based on dominant color:
    # If the color is very bright, recommend complementary colors, etc.
    recommendation_details = {
        "suggested_item": style_prediction["predicted_item"],
        "description": f"We recommend a {style_prediction['predicted_item']} that complements your dominant color {analysis_results['hex_color']}.",
        "affiliate_link": style_prediction["affiliate_link"]
    }
    return recommendation_details
