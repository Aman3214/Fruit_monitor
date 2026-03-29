const socket = io();
const MAX_LOGS = 5;

// Define Thresholds
const HUMIDITY_THRESHOLD = 80; // Example: Alert if above 80%
const GAS_THRESHOLD = 500;      // Example: Alert if above 500 PPM

const logBody = document.getElementById('log-body');

socket.on('ui_update', (data) => {
    // 1. Update Core Sensor Values
    document.getElementById('temp').innerText = data.temp;
    document.getElementById('hum').innerText = data.hum;
    document.getElementById('gas').innerText = data.gas;
    document.getElementById('confidence').innerText = data.confidence;

    // 2. Image Handling
    const cameraFeed = document.getElementById('camera-feed');
    if (data.image) {
        cameraFeed.src = data.image.startsWith('http') 
            ? data.image 
            : `data:image/jpeg;base64,${data.image}`;
    }

    // 3. Multi-Condition Alert Logic
    // Logic: Trigger if (AI says spoiled) OR (Hum is too high) OR (Gas is too high)
    const isHumidityUnsafe = data.hum > HUMIDITY_THRESHOLD;
    const isGasUnsafe = data.gas > GAS_THRESHOLD;
    const isAISpoiled = data.alert === true;

    const shouldAlert = isAISpoiled || isHumidityUnsafe || isGasUnsafe;

    const statusElement = document.getElementById('status');
    if (shouldAlert) {
        document.body.classList.add('spoilage-alert');
        
        // Dynamic Status Message
        if (isAISpoiled) statusElement.innerText = "SPOILAGE DETECTED (AI)";
        else if (isGasUnsafe) statusElement.innerText = "DANGEROUS GAS LEVELS";
        else if (isHumidityUnsafe) statusElement.innerText = "HIGH HUMIDITY WARNING";
        
        updateLogTable(data);
    } else {
        document.body.classList.remove('spoilage-alert');
        statusElement.innerText = "SYSTEM ONLINE";
    }
});

function updateLogTable(data) {
    const row = document.createElement('tr');
    const timestamp = new Date().toLocaleTimeString();

    row.innerHTML = `
        <td>${timestamp}</td>
        <td>${data.temp}°C</td>
        <td>${data.gas} PPM</td>
        <td>${data.confidence}%</td>
    `;

    logBody.prepend(row);
    while (logBody.children.length > MAX_LOGS) {
        logBody.removeChild(logBody.lastChild);
    }
}