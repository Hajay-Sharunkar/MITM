from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

app = FastAPI()

class Packet(BaseModel):
    packet_size: float
    src_port: float
    dst_port: float
    protocol: float
    tcp_len: float
    tcp_window: float
    time_delta: float

@app.get("/")
def home():
    return {"message": "MITM Detection API Running"}

@app.post("/predict")
def predict(packet: Packet):

    data = np.array([[
        packet.packet_size,
        packet.src_port,
        packet.dst_port,
        packet.protocol,
        packet.tcp_len,
        packet.tcp_window,
        packet.time_delta
    ]])

    data_scaled = scaler.transform(data)
    prob = model.predict_proba(data_scaled)[0][1]

    if prob > 0.7:
        result = "High Risk"
    elif prob > 0.4:
        result = "Suspicious"
    else:
        result = "Normal"

    return {
        "prediction": result,
        "attack_probability": float(prob)
    }
