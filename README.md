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