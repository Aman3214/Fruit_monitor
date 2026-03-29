import paho.mqtt.client as mqtt
import json
import time
import random

# Configuration
BROKER = "localhost"
TOPIC = "dashboard/update"

client = mqtt.Client()
client.connect(BROKER, 1883)

print("--- AI System Mock Started ---")
print("Monitoring Dashboard: http://localhost:3000")

try:
    while True:
        # Toggle Spoilage Logic
        is_spoiled = random.choice([True, False])
        
        # Prepare Payload
        payload = {
            "temp": round(random.uniform(25.0, 32.0) if is_spoiled else random.uniform(18.0, 22.0), 1),
            "hum": round(random.uniform(80.0, 95.0) if is_spoiled else random.uniform(50.0, 60.0), 1),
            "gas": random.randint(400, 600) if is_spoiled else random.randint(100, 150),
            "confidence": random.randint(75, 99) if is_spoiled else random.randint(5, 20),
            "alert": is_spoiled,
            "image": "https://placehold.co/600x400/000000/FFFFFF?text=" + ("SPOILED+FRUIT" if is_spoiled else "FRESH+FRUIT")
        }

        # Publish to Broker
        client.publish(TOPIC, json.dumps(payload))
        
        state = "ALERT (SPOILED)" if is_spoiled else "NORMAL (FRESH)"
        print(f"[{time.strftime('%H:%M:%S')}] State: {state} | Data Sent.")
        
        time.sleep(10)

except KeyboardInterrupt:
    print("\nTest Stopped.")
    client.disconnect()