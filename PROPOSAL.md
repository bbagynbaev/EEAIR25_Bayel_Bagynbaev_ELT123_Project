# Dust Dispersion Mapper: Spatial Tracking of PM2.5 / PM10 Particle Clouds Across Construction Sites

## 1. Executive Summary & Problem Statement

Dust generation on modern construction sites and industrial facilities poses severe environmental, operational, and occupational health risks. Fine particulate matter—specifically **PM2.5** (particles $\le 2.5\,\mu\text{m}$) and **PM10** (particles $\le 10\,\mu\text{m}$)—causes respiratory illness, reduces visibility, and often leads to non-compliance with municipal air quality regulations.

Existing air quality monitoring solutions rely primarily on static, single-point monitoring stations or expensive regulatory-grade enclosures. Single-point sampling fails to capture the spatial dynamics, movement vector, and concentration gradient of localized dust plumes caused by earthmoving, grinding, or wind erosion.

The **Dust Dispersion Mapper** project solves this limitation by deploying an autonomous, 3-node wireless sensor mesh utilizing low-cost SDS011 laser dust sensors, ESP32 microcontrollers, and peer-to-peer ESP-NOW communication. By feeding real-time spatial node readings into an Inverse Distance Weighting (IDW) interpolation engine, the system reconstructs particle cloud boundaries and maps dispersion dynamics across a site grid.

---

## 2. Core Research Question & Objectives

### Primary Research Question
> *"To what extent can spatial interpolation derived from a minimal 3-node sensor mesh accurately reconstruct dust cloud boundaries and concentration gradients across localized construction environments?"*

### Key Project Objectives
1. **Hardware Node Engineering:** Design and assemble 3 field-deployable sensor nodes, each integrating a Nova Fitness SDS011 laser sensor with an ESP32 microcontroller and autonomous battery power management.
2. **Ad-Hoc Wireless Networking:** Implement low-latency peer-to-peer data transmission using the **ESP-NOW** protocol to eliminate reliance on external Wi-Fi infrastructure or router hardware.
3. **Data Collection Hub:** Develop a central receiver node that aggregates telemetry frames, performs error checking, and outputs structured spatial-temporal datasets over Serial/Web interfaces.
4. **Spatial Interpolation Engine:** Develop a real-time spatial processing pipeline using Inverse Distance Weighting (IDW) to render continuous dust concentration heatmaps ($PM_{2.5}$ and $PM_{10}$).
5. **Experimental Boundary Analysis:** Quantify the accuracy, spatial resolution limits, and boundary fidelity of a 3-point spatial mesh under controlled dust dispersion conditions.

---

## 3. System Architecture & Component Specifications

```
                     ┌─────────────────────────────────────────┐
                     │          Sensing Node 1 (Tx)            │
                     │  ESP32 + SDS011 Laser Sensor (UART)     │
                     └────────────────────┬────────────────────┘
                                          │
                                       ESP-NOW
                                     (2.4GHz P2P)
                                          │
 ┌──────────────────────────────────┐     │     ┌──────────────────────────────────┐
 │       Sensing Node 2 (Tx)        ├─────┼─────┤       Sensing Node 3 (Tx)        │
 │  ESP32 + SDS011 Laser Sensor     │     │     │  ESP32 + SDS011 Laser Sensor     │
 └──────────────────────────────────┘     │     └──────────────────────────────────┘
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │       Data Collection Hub (Rx)          │
                     │     ESP32 Gateway Receiver              │
                     └────────────────────┬────────────────────┘
                                          │ Serial / Web
                                          ▼
                     ┌─────────────────────────────────────────┐
                     │    Spatial Interpolation Engine (IDW)   │
                     │   Python / Streamlit Real-Time Map      │
                     └─────────────────────────────────────────┘
```

### Hardware Specifications

| Component | Quantity | Functional Role | Operational Parameters |
| :--- | :--- | :--- | :--- |
| **Nova Fitness SDS011** | 3 units | PM2.5 & PM10 particle detection | Optical scattering, 0.3–10 $\mu\text{m}$ range, UART (9600 baud) |
| **ESP32 NodeMCU** | 4 units | Edge processing & communication | Dual-Core 240MHz, 2.4GHz ESP-NOW protocol, low power |
| **TP4056 + 18650 Li-Ion** | 3 sets | Node power supply | 3.7V / 2500mAh, regulated 5V step-up for fan & laser |
| **3D Weather Housings** | 3 units | Mechanical protection | Custom PETG/PLA enclosures with active airflow ventilation |

---

## 4. Mathematical Model & Spatial Interpolation

To reconstruct dust concentration boundaries across a 2D plane defined by node coordinates $(x_1, y_1)$, $(x_2, y_2)$, and $(x_3, y_3)$, the system utilizes **Inverse Distance Weighting (IDW)**.

The estimated concentration $Z(x, y)$ at any arbitrary grid coordinate $(x, y)$ is calculated as:

$$Z(x, y) = \frac{\sum_{i=1}^{3} w_i(x, y) \cdot Z_i}{\sum_{i=1}^{3} w_i(x, y)}$$

Where the distance-dependent weight $w_i(x, y)$ for node $i$ is defined by:

$$w_i(x, y) = \frac{1}{d\left((x, y), (x_i, y_i)\right)^p}$$

* **$Z_i$**: Measured dust concentration ($PM_{2.5}$ or $PM_{10}$ in $\mu\text{g}/m^3$) at node $i$.
* **$d(\cdot)$**: Euclidean distance between target point $(x,y)$ and node sensor location $(x_i, y_i)$.
* **$p$**: Distance decay power parameter (optimized at $p = 2$).

### Research Hypothesis
*A 3-node triangular mesh provides sufficient spatial gradient data to accurately infer the centroid and drift direction of a dust cloud within the convex hull of the sensors. However, spatial boundary reconstruction degrades rapidly beyond the triangle perimeter (extrapolation zone), highlighting geometric limits inherent to 3-point sensing topology.*

---

## 5. Implementation Roadmap & Grading Rubric Alignment

| Phase | Tasks & Technical Milestones | Targeted Rubric Criteria |
| :--- | :--- | :--- |
| **Phase 1: Setup & Schematic** | Circuit design, UART SDS011 driver testing, Proposal submission | Original Proposal & Analysis (10 pts) |
| **Phase 2: Firmware & ESP-NOW** | Peer-to-peer packet design, broadcast hub receiver code | Arduino Code & Comments (7 pts) |
| **Phase 3: Hardware Enclosure** | 3D CAD modeling, ventilation flow print, assembly & photos | 3D Models (3 pts) + Photos/Schematics (5 pts) |
| **Phase 4: Spatial Mapper** | IDW matrix calculation, Streamlit dashboard, cloud bounds | Code (7 pts) + Documentation (5 pts) |
| **Phase 5: Field Test & Video** | Controlled particulate test, footage recording (2–5 min) | Video Demonstration (10 pts) |
| **Phase 6: Final Analysis** | Git history cleanup, Outcomes & Limitations report | Commits (5 pts) + General Org (5 pts) |

---

## 6. Expected Project Deliverables

1. **GitHub Repository:** Fully documented source code, clean directory layout, hardware schematics, STL 3D models, and incremental commit history.
2. **Video Demonstration (2–5 mins):** Live demonstration of 3-node mesh reacting to dust generation, sending ESP-NOW telemetry, and rendering real-time IDW maps.
3. **Analytical Report (PDF):** Original project proposal paired with a rigorous analysis of experimental outcomes, accuracy limits, and system recommendations.