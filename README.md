# Dust Dispersion Mapper: Tracking PM2.5/PM10 Particle Clouds

> **Project Goal:** Real-time spatial tracking and boundary reconstruction of airborne dust clouds across construction sites using a 3-node wireless sensor mesh and Inverse Distance Weighting (IDW) interpolation.

![Dust Dispersion Map](python_viz/dust_dispersion_map.png)

---

## Project Overview
Monitoring airborne particulate matter ($PM_{2.5}$ and $PM_{10}$) on construction sites is critical for environmental compliance and worker safety. Standard single-point sensors fail to capture the movement and boundaries of dust clouds.

This project addresses the research question:  
**"Does spatial interpolation from a 3-node mesh accurately reconstruct dust cloud boundaries?"**

---

## 🛠 Hardware & System Architecture

The system consists of **3 Wireless Sensor Nodes** and **1 Central Hub**:

- **Sensor Nodes (x3):** ESP32 Microcontroller + Nova Fitness SDS011 Laser Dust Sensor.
- **Inter-Node Communication:** ESP-NOW Protocol (low-latency 2.4 GHz peer-to-peer communication without external Wi-Fi).
- **Data Hub (x1):** ESP32 connected to PC/laptop via USB Serial stream.
- **Power:** 18650 Li-ion batteries with TP4056 charging modules.

## Repository Structure
- `src/sensor_node/`: Firmware for the 3 sensing nodes (reads SDS011 UART and sends via ESP-NOW).
- `src/receiver_hub/`: Firmware for the central data collection hub.
- `python_viz/`: Python script implementing IDW spatial interpolation and heatmaps.
- `3d_models/`: STL files for 3D-printed weather-resistant sensor enclosures.
- `docs/`: Wiring diagrams, schematics, and high-resolution setup photos.

---

## Setup & Replication Instructions

### 1. Hardware Assembly
1. Connect SDS011 to ESP32:
   - `SDS011 TX` ──► `ESP32 RX2 (GPIO 16)`
   - `SDS011 RX` ──► `ESP32 TX2 (GPIO 17)`
   - `5V` & `GND` to power rails.
2. Flash `src/sensor_node/sensor_node.ino` to each of the 3 node ESP32s (update receiver MAC address in code).
3. Flash `src/receiver_hub/receiver_hub.ino` to the hub ESP32.

### 2. Running Python Visualization
```bash
cd python_viz
pip install -r requirements.txt
python dust_interpolation.py