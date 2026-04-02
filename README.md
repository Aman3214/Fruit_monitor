# Fruit Spoilage Monitoring System
A real-time IoT and Deep Learning solution for monitoring fruit health using **ESP32-CAM**, **MQTT**, and **MobileNetV2**.

---

## Project Structure

### Root Folder
* **`main.py`**: The central orchestrator. It uses `subprocess` with `cwd` (Current Working Directory) management to launch the Dashboard, AI Processor, and Mock Data scripts simultaneously, ensuring relative file paths are resolved correctly.
* **`test/test_output.py`**: Testing utility that simulates ESP32-CAM MQTT traffic (Base64 images and sensor data) for hardware-free debugging.

### AI Engine (/ai_engine)
* **`ai_processor.py`**: Core logic for MQTT subscription, image decoding, and TensorFlow inference.
* **`fruit_model.h5`**: The trained Keras/TensorFlow model file.
* **`env_requirements.txt`**: Python dependencies for the inference environment.

### Dashboard (/dashboard)
* **`server.js`**: Node.js backend handling Socket.io events and bridging MQTT data to the web interface.
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
   Ensure you have a Conda or virtual environment activated.
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

The system is designed to be launched from a single command. The `main.py` script manages the directory switching automatically.

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

## Transitioning from Mock to Real Hardware

To use the system with an actual **ESP32-CAM** instead of the simulation scripts:

### 1. Disable the Mock Stream
Open `main.py` and comment out the lines associated with the mock data process:
```python
# In main.py:
# mock_proc = subprocess.Popen(["python", MOCK_SCRIPT], cwd="test")
# processes.append(mock_proc)
```

### 2. Configure the ESP32-CAM
Update your Arduino sketch (`.ino`) with your computer's **Local IP Address**.
* Find your IP on Linux/Mac: `hostname -I`
* Find your IP on Windows: `ipconfig`

```cpp
// In your ESP32 Arduino code:
const char* mqtt_server = "192.168.1.XX"; // Your computer's IP
const char* topic = "esp32/cam_data";     // Match this in ai_processor.py
```

### 3. Network Security
Ensure both the ESP32 and the Computer are on the **same Wi-Fi network**. If the connection fails, allow incoming traffic on the MQTT port (1883) via your firewall.

---

## License
This project is licensed under the **MIT License**.