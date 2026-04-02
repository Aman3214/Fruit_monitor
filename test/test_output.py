import paho.mqtt.client as mqtt
import base64
import time
import os
import json
import random

# --- UPDATED CONFIGURATION ---
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
IMAGE_TOPIC = "esp32/camera" 
DATA_TOPIC = "hardware/data" 
TEST_IMAGE_DIR = "test_images"

client = mqtt.Client()

def send_mock_payload():
    # 1. Encode Image
    images = [f for f in os.listdir(TEST_IMAGE_DIR) if f.endswith(('.jpg', '.png'))]
    if not images: return
    
    with open(os.path.join(TEST_IMAGE_DIR, random.choice(images)), "rb") as f:
        img_str = base64.b64encode(f.read()).decode('utf-8')

    # 2. Create Combined Payload 
    # Ensure these keys match what your ai_processor.py 'json.loads' expects
    payload = {
        "image": img_str,
        "temp": round(random.uniform(22, 28), 1),
        "hum": round(random.uniform(50, 65), 1),
        "gas": random.randint(400, 700)
    }

    print(f"Sending combined payload to {DATA_TOPIC}...")
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.publish(DATA_TOPIC, json.dumps(payload))
    client.disconnect()

def run_mock_loop():
    client.connect("localhost", 1883, 60) # This is the connect_mqtt logic
    client.loop_start() # Starts a background thread to handle the connection
    
    try:
        while True:
            send_mock_payload() # Your function that publishes the image/json
            print("Mock data sent. Waiting 5 seconds...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping mock stream...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_mock_loop()