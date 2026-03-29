# Fruit Spoilage Monitoring System
A real-time IoT and Deep Learning solution for monitoring fruit health using **ESP32-CAM**, **MQTT**, and **MobileNetV2**.

---

## Project Structure

### Root Folder
* **`main.py`**: The primary execution script coordinating application logic and AI inference.
* **`mock_esp32.py`**: Testing utility that simulates ESP32-CAM MQTT traffic (images and sensor data) for hardware-free debugging.

### AI Engine (/ai_engine)
* **`ai_processor.py`**: Core logic for MQTT subscription and Base64 image processing.
* **`fruit_model.h5`**: The trained Keras/TensorFlow model file.
* **`env_requirements.txt`**: Python dependencies for the inference environment.
* **`test_ai_output.py`**: Standalone script to verify model predictions locally.

### Dashboard (/dashboard)
* **`server.js`**: Node.js backend handling Socket.io events and MQTT bridging.
* **`public/`**: Contains the frontend web assets.
    * **`index.html`**: The dashboard structure.
    * **`style.css`**: Visual styling and layout.
    * **`script.js`**: Frontend logic for real-time charts and data updates.

### Other Files (/other_files)
* **`fruit_trainer/`**: Complete pipeline for model development.
    * **`train_model.py`**: Transfer learning script using MobileNetV2.
    * **`requirements.txt`**: Training-specific dependencies.
    * **`dataset/`**: The structured image repository used during training.
    * **`FRUIT_16K/dataset_creation.py`**: Script to reorganize raw data into binary folders.
* **Hardware Design**:
    * **Pin Diagram**: Technical mapping of ESP32-CAM to MQ135 and DHT22.
    * **Circuit Diagram**: Schematic for the final hardware assembly.
    * **Case Assembly**: Files/instructions for the physical enclosure of the device.

---

## Technical Specifications
* **AI Model**: MobileNetV2 (Transfer Learning) optimized for 224x224 pixels.
* **Network Protocol**: MQTT (Mosquitto) on Port 1883.
* **Hardware Stack**: ESP32-CAM + MQ135 (Gas) + DHT22 (Temperature/Humidity).

---

## Installation and Setup

1. **Python Dependencies**:
   ```bash
   pip install -r ai_engine/env_requirements.txt
   ```

2. **Dashboard Setup**:
   ```bash
   cd dashboard
   npm install
   ```

---

## Testing and Verification

### Verifying AI Inference
To check if the trained model and the inference logic are working correctly without using the network or hardware:
1. Navigate to the `ai_engine` directory.
2. Run the test script:
   ```bash
   python test_ai_output.py
   ```
This script loads `fruit_model.h5`, processes a sample image, and prints the classification result (Fresh/Spoiled) to the console.

### Verifying Dashboard with Mock Data
To test the full system integration and Dashboard visualization without the ESP32-CAM hardware:
1. Ensure your MQTT Broker (Mosquitto) is running.
2. Start the Dashboard server:
   ```bash
   node dashboard/server.js
   ```
3. Run the mock script from the root folder:
   ```bash
   python mock_esp32.py
   ```
4. Open `http://localhost:3000` in your browser. The mock script streams simulated sensor data and images to verify that charts and camera feeds update in real-time.

---

## Execution for Final System
1. Start the MQTT broker (Mosquitto).
2. Run the main application: `python main.py`.
3. Start the dashboard: `node dashboard/server.js`.

---

## License
This project is licensed under the **MIT License**.

