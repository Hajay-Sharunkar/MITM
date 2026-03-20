import streamlit as st
import pandas as pd
import pickle
import pyshark
import time
import matplotlib.pyplot as plt

# Load model + scaler
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("🔐 MITM Attack Detection Dashboard")

# -------------------------------
# SECTION 1 — Manual Prediction
# -------------------------------
st.header("Manual Packet Check")

packet_size = st.number_input("Packet Size", min_value=0)
src_port = st.number_input("Source Port", min_value=0)
dst_port = st.number_input("Destination Port", min_value=0)
protocol = st.number_input("Protocol (6 = TCP)", min_value=0)

if st.button("Check Traffic"):
    data = pd.DataFrame(
        [[packet_size, src_port, dst_port, protocol]],
        columns=['packet_size','src_port','dst_port','protocol']
    )

    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)

    if prediction[0] == 1:
        st.error("🚨 ATTACK DETECTED")
    else:
        st.success("✅ SAFE TRAFFIC")


# -------------------------------
# SECTION 2 — Real-Time Detection
# -------------------------------
st.header("Real-Time Packet Detection")

run_capture = st.checkbox("Start Real-Time Detection")

attack_count = 0
safe_count = 0

if run_capture:
    st.warning("Running live capture...")

    capture = pyshark.LiveCapture(interface='eth0')

    output = st.empty()

    for packet in capture.sniff_continuously(packet_count=30):

        try:
            if hasattr(packet, 'tcp'):
                packet_size = int(packet.length)
                src_port = int(packet.tcp.srcport)
                dst_port = int(packet.tcp.dstport)
                protocol = 6

                data = pd.DataFrame(
                    [[packet_size, src_port, dst_port, protocol]],
                    columns=['packet_size','src_port','dst_port','protocol']
                )

                data_scaled = scaler.transform(data)
                prediction = model.predict(data_scaled)

                if prediction[0] == 1:
                    attack_count += 1
                    output.error(f"🚨 ATTACK: {src_port} → {dst_port}")
                else:
                    safe_count += 1
                    output.success(f"✅ SAFE: {src_port} → {dst_port}")

                time.sleep(0.2)

        except:
            continue


# -------------------------------
# SECTION 3 — Graph Visualization
# -------------------------------
st.header("Traffic Analysis")

if st.button("Show Traffic Graph"):

    labels = ['Safe Traffic', 'Attack Traffic']
    values = [safe_count, attack_count]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Traffic Classification")
    ax.set_ylabel("Packet Count")

    st.pyplot(fig)

    st.write(f"Safe Packets: {safe_count}")
    st.write(f"Attack Packets: {attack_count}")
