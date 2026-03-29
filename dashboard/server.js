const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const mqtt = require('mqtt');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Configuration
const PORT = 3000;
const MQTT_BROKER = 'mqtt://localhost'; 
const LOG_FILE = path.join(__dirname, '../logs/spoilage_report.json');

app.use(express.static('public'));

// Connect to MQTT Broker
const mqttClient = mqtt.connect(MQTT_BROKER);

mqttClient.on('connect', () => {
    console.log('Connected to MQTT Broker');
    mqttClient.subscribe('dashboard/update');
});

mqttClient.on('message', (topic, message) => {
    const data = JSON.parse(message.toString());

    // 1. Send data to the frontend via WebSockets
    io.emit('ui_update', data);

    // 2. Conditional Logging: Only if spoilage is detected (alert: true)
    if (data.alert === true) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            ...data
        };
        fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');
        console.log('Spoilage detected. Data logged to file.');
    }
});

server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});