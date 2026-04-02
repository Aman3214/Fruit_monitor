# Fruit Spoilage Monitoring System
A real-time IoT and Deep Learning solution for monitoring fruit health using **ESP32-CAM**, **MQTT**, and **MobileNetV2**.

---

## Project Structure

### Root Folder
* **`main.py`**: The central orchestrator. It uses `subprocess` with `cwd` management to launch the Dashboard, AI Processor, and Mock Data scripts simultaneously.
* **`test/test_output.py`**: Testing utility that simulates ESP32-CAM MQTT traffic (images and sensor data) for hardware-free debugging.

### AI Engine (/ai_engine)
* **`ai_processor.py`**: Core logic for MQTT subscription, image processing, and inference.
* **`fruit_model.h5`**: The trained Keras/Tensorflow model file.
* **`env_requirements.txt`**: Python dependencies for the inference environment.

### Dashboard (/dashboard)
* **`server.js`**: Node.js backend handling Socket.io events and MQTT bridging.
* **`public/`**: Frontend web assets.
    * **`index.html`**: The real-time dashboard UI.
    * **`script.js`**: Frontend logic for Socket.io and chart updates.

### Other Files (/other_files)
* **`fruit_trainer/`**: Complete pipeline for model development and dataset reorganization.
* **Hardware Design**: Circuit diagrams and pin mapping for ESP32-CAM, MQ135, and DHT22.

---

## Technical Specifications
* **AI Model**: MobileNetV2 optimized for 224x224 pixels.
* **Network Protocol**: MQTT (Mosquitto) on Port 1883.
* **Communication**: WebSockets (Socket.io) for real-time Frontend updates.
* **Hardware Stack**: ESP32-CAM, MQ135 (Gas), and DHT22 (Temp/Hum).

---

## Installation and Setup

1. **Environment Setup**:
   Ensure you have a Conda environment or virtual environment activated.
   ```bash
   pip install -r ai_engine/env_requirements.txt
   ```

2. **Dashboard Setup**:
   ```bash
   cd dashboard
   npm install
   ```

3. **MQTT Broker**:
   Ensure **Mosquitto** is installed and running on your system.
   ```bash
   sudo systemctl start mosquitto
   ```

---

## Execution

The system is designed to be launched from a single command. The `main.py` script handles the directory switching (CWD) automatically to ensure all relative file paths (like models and static assets) are resolved correctly.

### Full System Launch (Recommended)
From the **project root** directory:
```bash
python main.py
```
This will:
1. Start the **Node.js Dashboard** at `http://localhost:3000`.
2. Start the **AI Processor** to listen for incoming images.
3. Start the **Mock Data Stream** (for testing/presentation).

### Manual Execution (Individual Components)
If you prefer to run components in separate terminals:
* **Dashboard**: `cd dashboard && node server.js`
* **AI Engine**: `cd ai_engine && python ai_processor.py`
* **Mock Data**: `cd test && python test_output.py`

---

## Testing and Verification
To transition from testing to live hardware:
1. Open `main.py`.
2. Comment out the **Mock Data Section** (Step 3) in the `start_processes` function.
3. Power on the ESP32-CAM configured to point to your machine's IP address.

---

## License
This project is licensed under the **MIT License**.