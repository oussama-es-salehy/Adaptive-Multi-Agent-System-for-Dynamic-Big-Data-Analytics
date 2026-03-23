
# Adaptive-Multi-Agent-System-for-Dynamic-Big-Data-Analytics

# 📡 Distributed Multi-Agent Online Learning System  
## Real-Time Intrusion Detection with Concept Drift Detection

---

# 📌 1. Project Overview

This project implements a **Distributed Multi-Agent System (MAS)** for:

- Real-time network intrusion detection  
- Online Learning  
- Concept Drift Detection (ADWIN)  
- Dynamic Clustering  
- Big Data Streaming  

Technologies used:

- **Python**
- **SPADE** (Multi-Agent Framework)
- **Apache Kafka** (Streaming)
- **Spark Streaming** (Optional scaling)
- **River** (Online ML + ADWIN)

Dataset used:

- KDD Cup 99 Intrusion Detection Dataset

---

# 📊 2. Dataset

## 🎯 Problem Type
Multi-class Classification

## 📌 Objective
Detect network attacks in real-time.

Classes:
- normal
- dos
- probe
- r2l
- u2r

---

## 📥 Dataset Source

### Official Source (Recommended)

UCI Machine Learning Repository  
KDD Cup 1999 Dataset  

https://archive.ics.uci.edu/ml/datasets/kdd+cup+1999+data

---

### Improved Version (Recommended for Research)

NSL-KDD Dataset  

https://www.unb.ca/cic/datasets/nsl.html

---

# 🏗 3. System Architecture

```
              +------------------+
              |   KDD Dataset    |
              +------------------+
                       |
                       v
              +------------------+
              |  Kafka Producer  |
              +------------------+
                       |
                       v
        =================================
        |        Apache Kafka           |
        =================================
                       |
        ----------------------------------
        |                |               |
        v                v               v
+---------------+ +---------------+ +---------------+
| Data Agent    | | Learning Agent| | Drift Agent  |
| (Collector)   | | (River Model) | | (ADWIN)      |
+---------------+ +---------------+ +---------------+
                                         |
                                         v
                                +----------------+
                                | Cluster Agent  |
                                +----------------+
                                         |
                                         v
                                +----------------+
                                | Supervisor     |
                                +----------------+
```

---

# 🧠 4. Project Components

## 4.1 Data Streaming Layer

- Kafka Producer streams dataset line by line
- Simulates real-time big data

### Example Producer

```python
for row in dataset:
    producer.send("network_topic", value=row)
```

---

## 4.2 Multi-Agent System (SPADE)

Agents:

| Agent | Role |
|-------|------|
| DataAgent | Receives Kafka data |
| LearningAgent | Online classification |
| DriftAgent | Detect concept drift (ADWIN) |
| ClusterAgent | Dynamic clustering |
| SupervisorAgent | Global coordination |

---

## 4.3 Online Learning

Library: River

Example model:

```python
from river import linear_model, preprocessing

model = preprocessing.StandardScaler() | linear_model.LogisticRegression()
```

Learning is incremental:

```python
model.learn_one(x, y)
prediction = model.predict_one(x)
```

---

## 4.4 Concept Drift Detection

Algorithm: ADWIN

```python
from river.drift import ADWIN

drift_detector = ADWIN()

drift_detector.update(error)

if drift_detector.drift_detected:
    print("Drift detected!")
```

---

## 4.5 Dynamic Clustering

Algorithm options:

- Incremental KMeans
- DenStream
- DBSTREAM

Used to:
- Detect new attack patterns
- Adapt to evolving behavior

---

# 🔄 5. Concept Drift Simulation Strategy

Phase 1:
- Mostly normal traffic

Phase 2:
- Increase DOS attacks

Phase 3:
- Introduce new attack type

This simulates:
- Sudden drift
- Gradual drift
- Recurring drift

---

# 📈 6. Experimental Protocol

Compare:

1. Online Learning WITHOUT Drift Detection
2. Online Learning WITH ADWIN
3. MAS Architecture vs Centralized Model

Metrics:

- Accuracy
- Precision
- Recall
- F1-score
- Drift detection delay
- False drift alarms
- Model recovery time

---

# 🚀 7. Project Structure

```
distributed-drift-detection/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── kafka/
│   ├── producer.py
│   └── config.py
│
├── agents/
│   ├── data_agent.py
│   ├── learning_agent.py
│   ├── drift_agent.py
│   ├── cluster_agent.py
│   └── supervisor_agent.py
│
├── models/
│   ├── online_model.py
│   └── clustering.py
│
├── drift/
│   └── adwin_detector.py
│
├── streaming/
│   └── spark_streaming.py
│
├── evaluation/
│   └── metrics.py
│
├── main.py
└── README.md
```

---

# 🧪 8. Running the Project

## Step 1 – Start Kafka

```
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties
```

## Step 2 – Create Topic

```
kafka-topics.sh --create --topic network_topic --bootstrap-server localhost:9092
```

## Step 3 – Run Producer

```
python kafka/producer.py
```

## Step 4 – Run Multi-Agent System

```
python main.py
```

---

# 🎓 9. Research Contribution

This project demonstrates:

- Distributed AI architecture
- Real-time adaptive learning
- Autonomous agent collaboration
- Concept drift resilience
- Big Data streaming integration

---

# 🔥 10. Future Improvements

- Replace KDD with real network capture
- Deploy on Kubernetes
- Use Spark Structured Streaming
- Add Reinforcement Learning agent
- Add anomaly explanation module

---

# 🏁 Conclusion

This project combines:

✔ Multi-Agent Systems  
✔ Online Machine Learning  
✔ Concept Drift Detection  
✔ Big Data Streaming  
✔ Cybersecurity Application  

It represents a complete and publishable research system for adaptive intrusion detection in dynamic environments.

---
