# Raspberry Pi Sensor Suite  
Modular Python applications for integrating real hardware sensors with Domoticz using Redis and systemd-managed services.

## Overview  
This repository contains a set of lightweight Python applications designed to run on Raspberry Pi and integrate real environmental sensors with Domoticz.  
The system uses a clean, decoupled architecture:

- **Raspberry Pi Pico W** reads data from physical sensors (e.g., BME280, DHT22).  
- Sensor readings are sent over Wi‑Fi and stored in **Redis**.  
- The **virtualsensors** application reads these values from Redis and updates **virtual devices in Domoticz**.  
- The **watermeter** application counts pulses from a physical water meter and updates a Domoticz virtual counter **directly via the Domoticz API**.  
- Both applications run as **systemd services**, ensuring automatic startup, monitoring, and recovery.

This architecture ensures reliability, modularity, and easy scaling.

---

## System Architecture

```
Temperature, Humidity, Pressure sensors
[BME280,DHT22] → [Pico W] → WiFi → [Redis] → [domoticz_virtual_sensors.py] → [Domoticz]

Water Counter
[Hall Sensor] → [GPIO Raspbery Pi input] → [water_couter.service.py] → [Domoticz]
                                            
```

---

## Repository Structure  
Based on the current project layout:

```
4domoticz/
├── virtualsensors/
│   ├── domoticz_virtual_sensors.py
│   ├── domoticz_virtual_sensors.service
│   └── ...
├── water-couter/
    ├── water_couter.service.py
    ├── water_couter.service
    └── ...

```

---

## Components

### 1. virtualsensors  
A Python application that synchronizes real sensor data stored in Redis with virtual devices in Domoticz.

#### How it works
- Reads sensor values from Redis keys (e.g., `sensor:temperature`, `sensor:humidity`).  
- Maps Redis keys to Domoticz virtual device IDX numbers.  
- Updates Domoticz via its HTTP/JSON API.  
- Runs continuously as a **systemd service**.

#### Features
- Supports multiple sensor types (temperature, humidity, pressure, etc.).  
- Configurable Redis → Domoticz mapping.  
- Graceful handling of missing or stale data.  
- Lightweight and easy to extend.

---

### 2. Raspberry Pi Pico W (external component)  
Although not part of this repository, the Pico W is responsible for collecting real sensor data.

#### How it works
- Reads values from sensors such as **BME280**, **DHT22**, or others.  
- Sends measurements over Wi‑Fi to the Redis server.  
- Stores each reading under a dedicated Redis key.

#### Benefits
- Hardware layer is fully separated from the integration logic.  
- No need to connect sensors directly to the main Raspberry Pi.  
- Easy to add more sensors or more Pico W units.

---

### 3. watermeter  
A Python application that counts pulses from a water meter equipped with a reed switch or Hall sensor and updates a Domoticz virtual counter **directly**.

#### How it works
- Listens for pulses on a GPIO pin.  
- Each pulse represents a fixed volume of water (e.g., 1 pulse = 0.5 L).  
- **Immediately sends an update to Domoticz** using the `/json.htm?type=command&param=udevice` API endpoint.  
- Domoticz virtual counter increases with every pulse.  
- Runs continuously as a **systemd service**.  
- Maintains internal state to avoid losing counts during restarts.

#### Features
- Reliable pulse detection with hardware/software debounce.  
- Direct Domoticz integration — no Redis involved.  
- Real‑time updates for accurate consumption graphs.  
- Persistent counter state to prevent data loss.  
- Logging and diagnostics.

---

## systemd Integration  
Both applications include ready-to-use systemd service files.

### Installing a service  
Copy the service file to systemd:

```bash
sudo cp virtualsensors/domoticz_virtual_sensors.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable domoticz_virtual_sensors.service
sudo systemctl start domoticz_virtual_sensors.service
```

For the water meter:

```bash
sudo cp water-couter/water_couter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable water_couter.service
sudo systemctl start water_couter.service
```

### Checking status  
```bash
systemctl status domoticz_virtual_sensors.service
systemctl status water_couter.service
```

---

## Requirements 
- Raspberry Pi (any model with Python and GPIO support)  
- Raspberry Pi Pico W with connected sensors  
- Redis server  
- Python 3.8+  
- Domoticz with virtual devices configured  
- systemd (default on Raspberry Pi OS)

---

## Installation

```bash
git clone https://github.com/darton/4domoticz
cd 4domoticz
pip install -r requirements.txt
```

---

## Running Manually (for testing)

### virtualsensors
```bash
python virtualsensors/main.py
```

### watermeter
```bash
sudo python water-couter/main.py
```

---

## Configuration  
Each application contains its own configuration file or constants section where you can define:

- Redis host/port  
- Domoticz server address  
- Mapping of Redis keys to Domoticz IDX values  
- Pulse-to-volume conversion for the water meter  

---

## License  
This project is released under the MIT License.



- wersję README z diagramem graficznym,  
- przykładowe pliki konfiguracyjne,  
- albo dopracować strukturę repozytorium pod bardziej profesjonalny layout.
