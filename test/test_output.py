import paho.mqtt.client as mqtt
import base64
import time
import os
import json
import random

MQTT_BROKER = "localhost"
TOPIC_CAMERA = "esp32/camera" 
TOPIC_SENSORS = "esp32/sensors" 
TEST_IMAGE_DIR = "test_images"

client = mqtt.Client()

def send_separate_data():
    # 1. Send Sensor Data (Simulating the DHT22/MQ135 loop)
    sensor_payload = {
        "temp": round(random.uniform(22, 28), 1),
        "hum": round(random.uniform(50, 65), 1),
        "gas": random.randint(400, 700)
    }
    client.publish(TOPIC_SENSORS, json.dumps(sensor_payload))
    print(f"Published Sensors to {TOPIC_SENSORS}")

    # 2. Send Image Data (Simulating the Camera capture)
    images = [f for f in os.listdir(TEST_IMAGE_DIR) if f.endswith(('.jpg', '.png'))]
    if images:
        with open(os.path.join(TEST_IMAGE_DIR, random.choice(images)), "rb") as f:
            img_str = base64.b64encode(f.read()).decode('utf-8')
        client.publish(TOPIC_CAMERA, img_str)
        print(f"Published Image to {TOPIC_CAMERA}")

def run_mock_loop():
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    
    try:
        while True:
            send_separate_data()
            print("Cycle complete. Waiting 5 seconds...\n")
            time.sleep(5)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    run_mock_loop()