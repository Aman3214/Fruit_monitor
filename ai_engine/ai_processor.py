import os
import io
import json
import base64
import numpy as np
import paho.mqtt.client as mqtt
import tensorflow as tf
from PIL import Image

# Configuration & Model Loading
MODEL_PATH = "fruit_model.h5"
MQTT_BROKER = "localhost"
SUB_TOPIC = "hardware/data"
PUB_TOPIC = "dashboard/update"

print(f"Loading model from {MODEL_PATH}...")
model = tf.keras.models.load_model(MODEL_PATH)

IMG_HEIGHT = 224 
IMG_WIDTH = 224

def process_and_predict(base64_str):
    """Decodes image, resizes, and runs inference."""
    try:
        # Decode Base64 string to image bytes
        img_bytes = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Resize to model input size
        img = img.resize((IMG_HEIGHT, IMG_WIDTH))
        
        # Convert to numpy array and normalize (0-1)
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, 0) / 255.0
        
        # Run Inference
        predictions = model.predict(img_array)
        
        # Adjust logic if your model uses categorical (multi-class) output
        confidence = float(predictions) * 100
        is_spoiled = confidence > 75.0 # Threshold for Red Alert
        
        return round(confidence, 1), is_spoiled
    except Exception as e:
        print(f"Inference Error: {e}")
        return 0.0, False

def on_message(client, userdata, msg):
    """Triggered when new hardware data arrives."""
    try:
        data = json.loads(msg.payload)
        
        # Extract Image and run AI
        confidence, alert = process_and_predict(data['image'])
        
        # Enrich the payload for the dashboard
        processed_payload = {
            "temp": data.get('temp', 0),
            "hum": data.get('hum', 0),
            "gas": data.get('gas', 0),
            "image": data['image'],
            "confidence": confidence,
            "alert": alert
        }
        
        # Forward to Dashboard
        client.publish(PUB_TOPIC, json.dumps(processed_payload))
        print(f"Processed: Alert={alert} | Confidence={confidence}%")
        
    except Exception as e:
        print(f"Error in on_message: {e}")

# 2. MQTT Setup
client = mqtt.Client()
client.on_message = on_message

print(f"Connecting to broker at {MQTT_BROKER}...")
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(SUB_TOPIC)

print("AI Processor is online and listening for hardware data.")
client.loop_forever()