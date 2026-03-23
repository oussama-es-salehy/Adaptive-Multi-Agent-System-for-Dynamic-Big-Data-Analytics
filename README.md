# Distributed Multi-Agent Online Learning System for Real-Time Intrusion Detection

## 📡 1. Overview
This project implements a **Distributed Multi-Agent System (MAS)** for real-time network intrusion detection using online learning and concept drift detection.

## 🏗 2. Architecture
- **DataAgent**: Consumes data from Apache Kafka.
- **LearningAgent**: Performs online classification using River.
- **DriftAgent**: Detects concept drift using ADWIN.
- **ClusterAgent**: Performs incremental clustering.
- **SupervisorAgent**: Coordinates and monitors the global state.

## 🚀 3. Getting Started

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Kafka
For demonstration, make sure you have Kafka running on `localhost:9092`.

### Step 3: Run Producer
```bash
python -m kafka.producer
```

### Step 4: Run Multi-Agent System
```bash
python main.py
```

> [!NOTE]
> **SPADE Agents** require an XMPP server to communicate. You can use a local server (like Prosody) or a public one. If you are testing locally, ensure your server is running on `localhost`.

## 📊 4. Metrics
The system provides real-time evaluations:
- Accuracy, Precision, Recall, F1-score.
- Drift detection delay.

## 🎓 5. License
MIT
