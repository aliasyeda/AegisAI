# AegisAI

# AegisAI — NextGen Autonomous Cyber Defense & Awareness Intelligence Platform
<img width="1000" height="400" alt="image" src="https://github.com/user-attachments/assets/495def5b-4561-4a97-b7dd-792066acf3b7" />
<img width="1000" height="400" alt="image" src="https://github.com/user-attachments/assets/82d7dafa-d0ea-4c05-aee8-264a8498c032" />









AegisAI is an AI-powered cybersecurity platform designed to detect, analyze, explain, and respond to multiple categories of cyber threats through a unified system.

The project combines machine learning, explainable AI, confidence-based decision making, automated defense actions, SOC-style monitoring, threat logging, attack simulations, and cybersecurity awareness training in one platform.

> **Project type:** AI/ML + Cybersecurity
> **Primary ML model:** XGBoost
> **Interface:** Streamlit
> **Threat categories:** 6
> **Status:** Academic prototype / research-oriented proof of concept

---

## Overview

Modern cybersecurity systems often depend on separate tools for different threat types and can require significant manual analysis. AegisAI was developed to explore how machine learning and automation can be combined into a unified cybersecurity workflow.

The platform is designed around three main goals:

1. Detect multiple types of cyber threats.
2. Use prediction confidence to support explainable and automated defense decisions.
3. Combine technical detection with monitoring, simulation, and cybersecurity awareness.

The project covers six threat categories:

* Spam
* Phishing
* Malware
* DDoS
* IoT anomalies
* Weak/password-related security risks

The project report describes the implementation as a prototype and simulated cybersecurity environment rather than a full enterprise deployment.

---

## Key Features

### Multi-threat detection

AegisAI contains six specialized machine-learning detection modules:

* Spam detection
* Phishing detection
* Malware detection
* DDoS detection
* IoT anomaly detection
* Password security analysis

Each module uses domain-specific input features and an XGBoost-based classification approach.

### Explainable and confidence-based decisions

The system produces prediction probabilities/confidence information and uses these signals to support defense decisions.

Depending on the predicted risk, the system can perform actions such as:

* `ALLOW`
* `MONITOR`
* `QUARANTINE`
* `BLOCK`

This provides a simple confidence-gated approach to automated response rather than treating every prediction identically. The project architecture places this logic in the Confidence Gate System and ADRI (Autonomous Decision and Response Intelligence) layer.

### Centralized monitoring

The Streamlit interface provides a centralized dashboard for:

* Threat monitoring
* Alerts
* Security analytics
* Logs
* Threat history
* SOC-style operations
* Visualization

### SOC simulation

AegisAI includes a Security Operations Center simulation intended to model common monitoring and response workflows. The report includes dedicated SOC operations and real-world simulation components.

### Cybersecurity awareness

The platform also contains:

* Interactive quizzes
* Training material
* Attack simulations
* Explainability information

The purpose is to combine technical defense with user awareness rather than treating cybersecurity purely as a detection problem.

---

## System Architecture

AegisAI follows a three-tier architecture.

```text
                    ┌──────────────────────────────┐
                    │     Presentation Layer      │
                    │                              │
                    │  Streamlit UI               │
                    │  Dashboard                  │
                    │  SOC Operations Center      │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │      Business Logic Layer    │
                    │                              │
                    │  Threat Prediction Engine   │
                    │  ADRI                       │
                    │  Confidence Gate System     │
                    │  Simulation Engine          │
                    │  Defense Decision Logic     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │         Data Layer           │
                    │                              │
                    │  ML Models                  │
                    │  Threat Intelligence        │
                    │  Logs / Alerts               │
                    │  Explainability Data        │
                    │  Session State               │
                    └──────────────────────────────┘
```

The report describes the presentation, business-logic, and data layers and identifies the prediction engine, ADRI, confidence gates, simulation engine, unified models, threat intelligence storage, and session management as major components.

---

## Detection Workflow

The general machine-learning workflow is:

```text
Raw Cybersecurity Data
        │
        ▼
Data Collection
        │
        ▼
Preprocessing
        │
        ▼
Feature Extraction
        │
        ▼
XGBoost Classification
        │
        ▼
Threat Category + Probability
        │
        ▼
Confidence / Risk Decision
        │
        ├──► ALLOW
        ├──► MONITOR
        ├──► QUARANTINE
        └──► BLOCK
        │
        ▼
Logging / Monitoring / Alerting
```

For textual inputs, TF-IDF feature extraction is used. Numerical and behavioral features are used for areas such as malware, DDoS, and IoT detection.

---

## Threat Coverage

| Threat   | Main Approach                 | Example Features                                |
| -------- | ----------------------------- | ----------------------------------------------- |
| Spam     | TF-IDF + XGBoost              | Text patterns, suspicious keywords              |
| Phishing | URL features + XGBoost        | URL length, HTTPS, redirects, domain behavior   |
| Malware  | Behavioral features + XGBoost | Entropy, API usage, execution behavior          |
| DDoS     | Traffic analysis + ML         | Packet rate, traffic spikes, source IP behavior |
| IoT      | Behavioral/anomaly analysis   | Device activity, communication patterns         |
| Password | TF-IDF + classification       | Weak/common patterns, password structure        |

The project report documents these six detection categories and their associated feature types.

---

## Datasets

The project uses separate cybersecurity datasets for the different detection tasks.

| Dataset  |         Size | Main Input                |
| -------- | -----------: | ------------------------- |
| Spam     |    5,572 × 2 | SMS/message text          |
| Phishing |  10,000 × 50 | URL security features     |
| Malware  | 100,000 × 25 | Malware behavior/features |
| DDoS     |  42,300 × 22 | Network traffic           |
| IoT      | 357,953 × 13 | IoT activity behavior     |
| Password |       ~1,000 | Password patterns         |

The presentation describes the dataset dimensions and the main feature types used for each category.

> **Note:** Raw datasets should only be included in this repository when their licenses allow redistribution. Otherwise, document the dataset source and provide instructions for obtaining it separately.

---

## Machine Learning Approach

### Why XGBoost?

XGBoost was selected as the primary classifier because the project uses a combination of structured cybersecurity features and probability-based decisions.

The project report identifies the following practical reasons for its use:

* Fast training and inference
* Good performance on structured data
* Boosting-based reduction of overfitting
* Feature importance support
* Suitability for real-time classification
* Probability outputs that can support automated defense decisions

### Feature Extraction

Different threat categories require different representations.

For text-based data, AegisAI uses TF-IDF. Other modules use domain-specific numerical or behavioral features such as:

* URL characteristics
* Network traffic statistics
* File entropy
* API/execution behavior
* IoT communication patterns
* Password structure

---

## Autonomous Defense Logic

AegisAI does not simply return a threat label. The predicted probability is also used as an input to the defense decision process.

Example:

```text
Prediction
    │
    ▼
Threat probability
    │
    ▼
Confidence gate
    │
    ├── Low risk  ─────► ALLOW
    │
    ├── Moderate ─────► MONITOR / QUARANTINE
    │
    └── High risk ────► BLOCK
```

The project includes examples where highly suspicious inputs are blocked, moderately suspicious inputs are quarantined or monitored, and legitimate inputs are allowed.

---

## Example Outputs

### Spam

```text
FREE MONEY NOW!!!            → 0.95 → BLOCK
Hello, how are you?          → 0.18 → ALLOW
URGENT: Your account...      → 0.73 → QUARANTINE
```

### Phishing

```text
Verify your bank account     → 0.91 → BLOCK
Password reset required      → 0.76 → QUARANTINE
Team meeting scheduled       → 0.22 → ALLOW
```

### Malware

```text
Low entropy / low activity   → 0.30 → ALLOW
Suspicious behavior          → 0.60 → MONITOR
High entropy / abnormal APIs → 0.89 → QUARANTINE
```

### DDoS

```text
Normal traffic               → 0.25 → ALLOW
Abnormal traffic spike       → 0.74 → QUARANTINE
Large multi-IP traffic spike → 0.98 → BLOCK
```

These examples are taken from the project’s documented model-output and defense-response evaluation.

---

## Technology Stack

### Core

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost

### Feature Extraction

* TF-IDF
* Domain-specific numerical and behavioral features

### Interface and Visualization

* Streamlit
* Plotly
* Matplotlib

### Supporting Tools

* Joblib
* Requests
* Pillow

The report specifies Python 3.8+, Streamlit, Pandas, NumPy, Scikit-learn, XGBoost, Plotly, Matplotlib, Joblib, Requests, and Pillow as part of the technology stack.

---

## Repository Structure

```text
AegisAI/
│
├── app.py
├── unified_defender.py
├── requirements.txt
│
├── models/
│   ├── spam_xgboost_model.pkl
│   ├── phishing_xgboost_model.pkl
│   ├── malware_xgboost_model.pkl
│   ├── ddos_xgboost_model.pkl
│   ├── iot_xgboost_model.pkl
│   └── password_xgboost_model.pkl
│
├── utils/
│   └── ...
│
├── check/
│   └── ...
│
├── Test Samples/
│   └── ...
│
├── ALL DEMO SAMPLES WITH LOGS.md
├── MORE SAMPLES.md
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aliasyeda/AegisAI.git
cd AegisAI
```

### 2. Create a virtual environment

```bash
python -m venv aegisai_env
```

### 3. Activate the environment

#### Windows

```bash
aegisai_env\Scripts\activate
```

#### Linux / macOS

```bash
source aegisai_env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## System Requirements

The project report describes a minimum development/testing configuration of:

* Python 3.8+
* 8 GB RAM
* 10 GB storage
* Windows 10+, Ubuntu 18.04+, or macOS 10.15+
* Stable network connection

The report also proposes a stronger production configuration for larger workloads, but the current project should be understood as a prototype/simulated environment rather than a production security product.

---

## Testing

AegisAI was tested at several levels:

### Unit Testing

Individual detection and system components were tested independently.

### Integration Testing

Integration testing checked communication between:

* Frontend and ML models
* Datasets and prediction models
* Prediction models and defense actions
* Monitoring and logging components

### Functional Testing

The six detection modules were tested using representative cybersecurity scenarios.

### Interface Testing

The Streamlit interface, alerts, graphs, navigation, logs, and monitoring panels were also tested.

---

## Awareness Module Evaluation

The project also evaluated its cybersecurity training component.

Reported results were:

* Pre-training accuracy: ~45%
* Post-training accuracy: ~88–92%
* Knowledge retention after 30 days: ~80%

These figures come from the project's quiz/training evaluation section.

---

## Results

During testing, the project demonstrated:

* Detection across all six implemented threat categories
* Confidence-based defense actions
* Real-time monitoring and alerting
* Automated `ALLOW`, `MONITOR`, `QUARANTINE`, and `BLOCK` responses
* Threat logging and historical tracking
* Integrated dashboard and SOC-style monitoring
* Cybersecurity awareness and simulation modules

The report describes the system as showing strong classification performance and fast autonomous response during its experimental evaluation.

---

## Limitations

AegisAI is primarily a practical prototype and simulated cybersecurity environment. Its performance therefore depends on the quality, coverage, and distribution of the datasets used for training and evaluation.

A model that performs well on the project's datasets may not generalize to unseen attacks, changing attacker behavior, or real-world operational environments. The current system also relies on predefined threat categories and therefore does not cover the full range of possible cyberattack behaviors.

The project does not represent a complete enterprise-grade SOC or a validated production defense system. Real-world deployment would require broader datasets, stronger external validation, adversarial testing, continuous monitoring, operational safeguards, and evaluation against evolving threats.

This limitation is explicitly consistent with the project report's description of AegisAI as a prototype/simulation rather than full-scale enterprise deployment.

---

## Research and Evaluation Considerations

One lesson from developing AegisAI is that high benchmark or test performance alone does not establish that a cybersecurity model is robust in real-world conditions.

Important future evaluation dimensions include:

* Generalization to unseen threats
* Distribution shift
* False positives and false negatives
* Confidence calibration
* Adversarial inputs
* Response consistency
* Detection-to-response latency
* Human oversight of autonomous actions
* Robustness across different data sources

This is particularly relevant when considering machine-learning systems for cybersecurity, where detection quality and the consequences of incorrect automated actions are both important.

---

## Future Scope

The project identifies several possible extensions:

* Ransomware detection
* Cryptojacking detection
* Supply-chain attack detection
* Mobile application support
* Email gateway integration
* Automated scheduled reports
* Decentralized threat-intelligence sharing
* Quantum-resistant cryptography
* Full SOAR capabilities

These are proposed future directions rather than capabilities currently claimed as implemented.

---

## Deployment Options

The project report discusses several possible deployment models:

* SaaS
* On-premises
* Hybrid
* Containerized deployment using Docker/Kubernetes
* Virtual appliance deployment

These are deployment options discussed by the project design and should not be interpreted as proof that all of them are currently deployed in production.

---

## Project Documentation

This repository contains the implementation and supporting materials for the AegisAI project.

Additional project documentation can include:

* Project report
* Presentation
* Sample threat inputs
* Sample model outputs
* Demonstration logs
* Screenshots

---

## References

* XGBoost Documentation — https://xgboost.readthedocs.io/
* Scikit-learn Documentation — https://scikit-learn.org/
* Streamlit Documentation — https://streamlit.io/
* Pandas Documentation — https://pandas.pydata.org/
* NumPy Documentation — https://numpy.org/
* Kaggle Datasets — https://www.kaggle.com/datasets

---

## Authors

## Syeda Alia Samia

AegisAI was developed as a final-year major project in Computer Science and Engineering (IoT, Cybersecurity including Blockchain Technology)
