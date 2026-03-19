# PhantomGuard 2.0 - Final OpenSpec (Full System)

## 0. Meta
name: PhantomGuard 2.0  
type: full-stack-ai-cybersecurity-system  
architecture: agent + backend + frontend  
development_mode: spec-driven  

---

## 1. Overview
PhantomGuard 2.0 is a full-stack AI-based cybersecurity system that detects ransomware and abnormal system behavior in real time. It combines a Python monitoring agent, a FastAPI backend, and a React dashboard.

The system detects:
- Suspicious downloads from browser
- Abnormal file activity (ransomware patterns)
- Honeyfile access
- Behavioral anomalies using BiLSTM

---

## 2. Core Objectives
- Real-time ransomware detection
- Detect browser-induced threats (downloads)
- Monitor file system activity
- Provide alerts via React dashboard
- Visualize detection flow clearly
- Demonstrate AI + rule-based hybrid detection

---

## 3. System Architecture

### 3.1 Frontend (React)
Responsibilities:
- Login/Register UI
- Dashboard visualization
- Alerts display
- Graphs and analytics
- Animated detection flow

Components:
- LoginPage
- RegisterPage
- Dashboard
- AlertsPanel
- GraphPanel
- FlowVisualizer

---

### 3.2 Backend (FastAPI)
Responsibilities:
- API handling
- Authentication (JWT)
- Store logs and alerts
- Communicate with agent

Endpoints:
- POST /register
- POST /login
- POST /logs
- GET /alerts
- GET /stats

---

### 3.3 Python Agent
Responsibilities:
- Monitor system activity
- Detect abnormal behavior
- Extract features
- Send logs to backend

Modules:
- monitor.py → file & process tracking
- detector.py → AI + rule-based detection
- sender.py → API communication

---

## 4. Detection System

### 4.1 Browser Detection (Indirect)
- Detect downloads in Downloads folder
- Track process (chrome.exe, edge.exe)
- Monitor file creation after download

### 4.2 File Monitoring
- Detect file open/change
- Detect rapid modifications
- Monitor Documents/Desktop folders

### 4.3 Honeyfiles
- Create hidden decoy files
- Trigger alert if accessed

---

## 5. Detection Logic (Hybrid)

Trigger alert if ANY:

- BiLSTM predicts attack
- Z-score > 3
- Entropy > 7.5
- Honeyfile accessed
- Rapid file modifications detected

---

## 6. Data Specification

Features:
- timestamp
- file_change_rate
- cpu_usage
- entropy
- process_name
- file_path

Label:
- 0 = normal
- 1 = ransomware

Sequence:
- length: 10

---

## 7. Model Specification

Model: BiLSTM  
Input: (sequence_length, features)  
Output: binary classification  

Layers:
- Bidirectional LSTM (64)
- Dense (32)
- Dense (1 sigmoid)

---

## 8. Workflow

1. User logs into React dashboard
2. Agent monitors system activity
3. Browser download or file activity occurs
4. Features extracted
5. Passed to BiLSTM + rules
6. Detection triggered
7. Log sent to backend
8. Dashboard updates in real time

---

## 9. Dashboard Design

### Sections:

#### System Status
- Green → Normal
- Red → Alert

#### Alerts Panel
- File name
- Process name
- Timestamp
- Risk level

#### Graphs
- File activity over time
- CPU usage
- Detection spikes

#### Flow Visualizer
Animated pipeline:
Browser → Agent → Features → Model → Detection → Alert → Dashboard

---

## 10. Demo Scenario

1. Login to dashboard
2. Open browser and download file
3. Agent detects file creation
4. Detection triggered
5. Alert shown on dashboard
6. Flow animation highlights steps

---

## 11. API Contract

POST /logs
- file
- process
- entropy
- prediction

GET /alerts
- list of alerts

---

## 12. Folder Structure

/phantomguard
│
├── frontend (React UI)
├── backend (FastAPI)
├── agent (Python monitoring)
├── model (BiLSTM)
├── data (logs)
├── specs (spec files)

---

## 13. Constraints

- No direct browser URL tracking
- No kernel-level access
- User-mode monitoring only

---

## 14. Success Criteria

- Detect abnormal activity
- Show real-time alerts
- Clear visualization of detection flow
- Smooth UI experience

---

## 15. Future Enhancements

- Kernel-level monitoring
- Multi-device support
- Cloud-based intelligence
- Explainable AI (XAI)

---

## 16. Viva Explanation (Key Point)

“Instead of directly tracking websites, the system detects browser-induced malicious activities such as suspicious downloads and abnormal file behavior using AI and behavioral analysis.”

---
