# SentinelMesh

## Agentic AI–Driven Cloud-Scale OT/IoT Deception & Isolation Platform

SentinelMesh is a cloud-native security platform that simulates industrial IoT environments, detects device compromise using network physics and behavioral intelligence, and silently isolates attackers into a deception environment without interrupting device availability.

It models real industrial architectures while remaining fully deployable on AWS for demonstration and research purposes.

---

## Overview

Modern IoT and OT devices are vulnerable to reconnaissance, manipulation, and man-in-the-middle attacks. SentinelMesh converts EC2 instances into high-fidelity industrial devices (PLCs, cameras, sensors) and protects them using a layered detection and isolation system.

If a device behaves suspiciously, SentinelMesh changes its *network reality* and moves the attacker into a deception cloud—where all activity is monitored but poses no risk.

---

## Key Features

* High-fidelity device simulation using EC2
* Behavioral and network-physics–based anomaly detection (MITM, recon)
* Agentic AI for risk scoring and decision-making
* Deterministic Control Agent for enforcement
* Zero lateral movement through micro-segmentation
* Cloud-based OT/IT boundary enforcement
* Real-time deceptive rerouting via Security Group switching
* Live network topology visualization
* Integration with AWS IoT Core, CloudWatch ML, RDS, and S3

---

## Architecture

```
Attacker
   ↓
EC2 Fake Device (PLC / Camera / Sensor)
   ↓  (MQTT + TLS, X.509 Identity)
AWS IoT Core (Production Endpoint)
   ↓
IoT Rules Engine
   ├─ CloudWatch Metrics & ML Detection
   ├─ Agentic AI (Behavioral & MITM Analysis)
   └─ RDS / Grafana (State & Visualization)
        ↓
Control Agent (Deterministic Enforcement)
        ↓
Security Group Switch (Reality Change)
        ↓
AWS IoT Core (Deception Endpoint)
```

**Key principle:** Devices remain where they are; only the network pathways around them change.

---

## System Components

### 1. Simulated OT/IoT Devices (EC2)

Devices emulate:

* PLCs
* IP cameras
* Industrial sensors

Each EC2 instance:

* Runs fake OT services (Modbus, RTSP, HTTP)
* Publishes telemetry and network physics to IoT Core
* Uses per-device certificates and secure MQTT

### 2. Agentic AI

Runs as a cloud service but logically belongs to the OT side.
Responsibilities:

* Baseline learning
* Behavioral anomaly detection
* MITM detection via timing drift
* Recon pattern identification
  Outputs decisions only; it never touches infrastructure.

### 3. Control Agent

A deterministic executor (Lambda or EC2) that:

* Applies isolation
* Modifies Security Groups
* Redirects compromised devices to deception infrastructure
* Logs all actions

The Control Agent performs actions the AI recommends.

### 4. Deception Environment

A separate AWS IoT Core endpoint where:

* Fake digital twins respond to attacker commands
* Synthetic telemetry is generated
* PCAP and payload collection occurs
* Attacker interaction is safely contained

---

## Network Physics Detection

MITM attacks introduce unavoidable timing anomalies:

* Increased RTT
* Jitter instability
* Modified TLS handshake times
* MQTT ACK delays
* TCP retransmissions

SentinelMesh tracks:

* Round-trip times
* Latency drift
* Transport errors
* Timing baselines

CloudWatch ML performs metric anomaly detection.
Agentic AI validates context and produces final decisions.

---

## Zero Trust & OT/IT Separation

SentinelMesh enforces:

* No device-to-device communication
* One-way OT → IT telemetry
* No inbound cloud commands to devices
* Per-device identity and RBAC
* Micro-segmented EC2 isolation
* Segregated production and deception realities

A compromised device cannot affect any other device.

---

## Data Management

* **RDS**

  * Device state
  * Risk scores
  * Isolation events
  * AI decisions

* **CloudWatch ML**

  * Metric anomaly detection

* **S3**

  * PCAPs
  * Payloads
  * Attacker artifacts

* **Discarded**

  * High-volume raw telemetry
  * Raw physics metrics

Only meaningful intelligence is stored.

---

## Live Topology Visualization

Grafana Node Graph Panel shows:

* Device state (Production or Deception)
* Backend routing
* Isolation events in real time
* Attack progression

Topology updates based on RDS data and Control Agent actions.

---

## Demo vs Real-World Deployment

| Component | Demo (Cloud-Only) | Production (Hybrid)       |
| --------- | ----------------- | ------------------------- |
| Devices   | EC2               | Physical IoT/PLC hardware |
| AI        | Cloud             | On-premise edge           |
| Isolation | SG switching      | OT firewall segmentation  |
| Deception | Cloud-based       | Digital twin replicas     |
| Data flow | MQTT to IoT Core  | MQTT + on-prem brokers    |

The conceptual architecture remains identical.
---