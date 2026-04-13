import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="MITM Detection", layout="centered")

st.title("🔐 MITM Attack Detection System")

# -------------------------------
# LOAD MODEL
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "scaler.pkl"), "rb"))

# -------------------------------
# INPUT
# -------------------------------
st.subheader("🧪 Enter Packet Details")

packet_size = st.number_input("Packet Size", value=100)
src_port = st.number_input("Source Port", value=50000)
dst_port = st.number_input("Destination Port", value=5000)
protocol = st.selectbox("Protocol", [6])
tcp_len = st.number_input("TCP Length", value=20)
tcp_window = st.number_input("TCP Window Size", value=64240)
time_delta = st.number_input("Time Delta", value=0.001)

# -------------------------------
# PREDICTION
# -------------------------------
if st.button("Analyze"):

    data = pd.DataFrame(
        [[packet_size, src_port, dst_port, protocol, tcp_len, tcp_window, time_delta]],
        columns=[
            "packet_size","src_port","dst_port","protocol",
            "tcp_len","tcp_window","time_delta"
        ]
    )

    data_scaled = scaler.transform(data)
    prob = model.predict_proba(data_scaled)[0][1]

    if prob > 0.7:
        st.error(f"🚨 High Risk ({prob:.2f})")
    elif prob > 0.4:
        st.warning(f"⚠️ Suspicious ({prob:.2f})")
    else:
        st.success(f"✅ Normal ({prob:.2f})")

# -------------------------------
# ROC CURVE
# -------------------------------
st.subheader("📈 Model Performance")

try:
    data = pd.read_csv(os.path.join(BASE_DIR, "final_dataset.csv"))

    data.columns = [
        "packet_size","src_port","dst_port","protocol",
        "tcp_len","tcp_window","time_delta","label"
    ]

    # CLEAN DATA
    data = data.replace(r"[^\d\.]", "", regex=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.dropna()

    X = data[[
        "packet_size","src_port","dst_port","protocol",
        "tcp_len","tcp_window","time_delta"
    ]]

    y = data["label"]

    X_scaled = scaler.transform(X)
    y_prob = model.predict_proba(X_scaled)[:,1]

    fpr, tpr, _ = roc_curve(y, y_prob)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots()
    ax.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    ax.plot([0,1],[0,1],'--')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()

    st.pyplot(fig)

except Exception as e:
    st.error(f"ROC Error: {e}")
