import paho.mqtt.client as mqtt
import json
import base64
import time
import random

# Use a small sample image file or a placeholder string
DUMMY_IMAGE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

client = mqtt.Client()
client.connect("localhost", 1883)

print("Starting Mock ESP32-CAM Simulator...")

while True:
    payload = {
        "temp": round(random.uniform(20.0, 25.0), 2),
        "hum": round(random.uniform(60.0, 70.0), 2),
        "gas": random.randint(100, 200),
        "image": DUMMY_IMAGE_BASE64
    }
    
    client.publish("hardware/data", json.dumps(payload))
    print(f"Sent Mock Data: Temp {payload['temp']}°C")
    time.sleep(10)