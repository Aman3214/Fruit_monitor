import os
import io
import json
import base64
import numpy as np
import paho.mqtt.client as mqtt
import tensorflow as tf
from PIL import Image

# Configuration
MODEL_PATH = "fruit_model.h5"
MQTT_BROKER = "localhost"
TOPIC_SENSORS = "esp32/sensors"
TOPIC_CAMERA = "esp32/camera"
PUB_TOPIC = "dashboard/update"

print(f"Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# State Buffer: Holds the last known sensor values
latest_telemetry = {"temp": 0, "hum": 0, "gas": 0}

def process_and_predict(base64_str):
    try:
        img_bytes = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img = img.resize((224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, 0) / 255.0
        
        predictions = model.predict(img_array)
        confidence = float(predictions) * 100
        return round(confidence, 1), confidence > 75.0
    except Exception as e:
        print(f"Inference Error: {e}")
        return 0.0, False

def on_message(client, userdata, msg):
    global latest_telemetry
    try:
        # Update Sensors State
        if msg.topic == TOPIC_SENSORS:
            latest_telemetry.update(json.loads(msg.payload))
            print("Telemetry Cache Updated")

        # Process Image and Publish Combined Data
        elif msg.topic == TOPIC_CAMERA:
            img_str = msg.payload.decode('utf-8')
            confidence, alert = process_and_predict(img_str)
            
            # Late-Stage Fusion: Combine cached sensors with current image AI
            processed_payload = {
                **latest_telemetry,
                "image": img_str,
                "confidence": confidence,
                "alert": alert
            }
            
            client.publish(PUB_TOPIC, json.dumps(processed_payload))
            print(f"Update Sent: Confidence {confidence}% | Alert: {alert}")
            
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

# Subscribe to both independent hardware streams
client.subscribe([(TOPIC_SENSORS, 0), (TOPIC_CAMERA, 0)])

print("AI Processor: Listening for separate Sensor and Camera streams...")
client.loop_forever()