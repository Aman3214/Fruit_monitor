0#include "esp_camera.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include "base64.h"
// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "YOUR_BROKER_IP"; // e.g., 192.168.1.5

// --- Pin Definitions ---
#define DHTPIN 14
#define DHTTYPE DHT22
#define MQ135_PIN 12 

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

// Camera Settings (AI-Thinker)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setupCamera() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;

    if(psramFound()){
        config.frame_size = FRAMESIZE_QVGA; // 320x240 for AI processing
        config.jpeg_quality = 12;
        config.fb_count = 2;
    } else {
        config.frame_size = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
    }

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) { Serial.printf("Camera init failed"); return; }
}

void setup() {
    Serial.begin(115200);
    dht.begin();
    setupCamera();

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    
    client.setServer(mqtt_server, 1883);
    // Increase buffer for Base64 image strings
    client.setBufferSize(20000); 
}

void loop() {
    if (!client.connected()) {
        while (!client.connected()) {
            if (client.connect("ESP32CAM_Client")) {
                Serial.println("MQTT Connected");
            } else {
                delay(5000);
            }
        }
    }
    client.loop();

    // 1. Capture Image
    camera_fb_t * fb = esp_camera_fb_get();
    if (fb) {
        // Correct native ESP32 way to encode
        String base64Image = base64::encode(fb->buf, fb->len);
        
        // Publish to MQTT
        client.publish("esp32/camera", base64Image.c_str());
        
        // Return the frame buffer to memory
        esp_camera_fb_return(fb);
    }

    // 2. Read Sensors
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    int gasRaw = analogRead(MQ135_PIN);

    // 3. Publish Telemetry (JSON format)
    String telemetry = "{\"temp\":" + String(t) + ",\"hum\":" + String(h) + ",\"gas\":" + String(gasRaw) + "}";
    client.publish("esp32/sensors", telemetry.c_str());

    delay(2000); // Sampling rate
}
