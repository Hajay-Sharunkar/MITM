# 🔐 MITM Attack Detection System using Machine Learning

## 🌐 Live Demo

👉 https://mitm-detection.streamlit.app/

---

## 📌 Overview

This project demonstrates how **Man-in-the-Middle (MITM) attacks** can be detected using **Machine Learning (XGBoost)** based on network packet features.

The system analyzes packet-level data and classifies traffic as:

* ✅ Normal
* ⚠️ Suspicious
* 🚨 High Risk

---

## 🎯 Problem Statement

Detecting MITM attacks in network traffic is challenging due to:

* Large volume of data
* Dynamic attack behavior
* Lack of adaptive detection systems

---

## 💡 Solution

A **Machine Learning-based detection system** that:

* Learns patterns from network traffic
* Classifies packets based on behavior
* Provides probability-based risk assessment

---

## 🧠 Technologies Used

* Python
* XGBoost (Machine Learning)
* Scikit-learn
* Pandas & NumPy
* Streamlit (UI)
* Matplotlib (Visualization)

---

## ⚙️ System Architecture

```text
User Input → Feature Processing → ML Model → Prediction → Visualization
```

---

## 📊 Features

✔ Packet-level anomaly detection
✔ Probability-based prediction
✔ Interactive Streamlit UI
✔ ROC Curve visualization
✔ Clean and interpretable outputs

---

## 📁 Project Structure

```text
MITM/
├── app.py                # Streamlit UI
├── train_model.py        # Model training
├── model.pkl             # Trained model
├── scaler.pkl            # Feature scaler
├── final_dataset.csv     # Dataset
├── requirements.txt      # Dependencies
└── README.md
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/MITM.git
cd MITM
```

### 2️⃣ Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Train the model

```bash
python train_model.py
```

### 5️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📈 Model Performance

* Accuracy: ~99%
* ROC-AUC Score: ~0.99

> Note: Performance depends on dataset quality.

---

## ⚠️ Limitations

* Uses packet-level data only
* Limited dataset size
* Not real-time detection system

---

## 🚀 Future Improvements

* Real-time packet monitoring
* Flow-based analysis
* Deep learning models
* Cloud deployment with scalability

---

## 🧠 Learning Outcomes

* Network traffic analysis
* Cybersecurity fundamentals
* Machine learning implementation
* Data preprocessing & feature engineering

---

## 👨‍💻 Author

**Hajay Sharunkar**

---

## ⭐ Show your support

If you like this project, give it a ⭐ on GitHub!
