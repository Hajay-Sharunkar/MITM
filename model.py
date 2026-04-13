import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier

# -------------------------------
# LOAD DATA
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "final_dataset.csv")

data = pd.read_csv(data_path)

# Set proper column names
data.columns = [
    "packet_size","src_port","dst_port","protocol",
    "tcp_len","tcp_window","time_delta","label"
]

# -------------------------------
# CLEAN DATA (IMPORTANT)
# -------------------------------
data = data.replace(r"[^\d\.]", "", regex=True)
data = data.apply(pd.to_numeric, errors='coerce')
data = data.dropna()

print("Clean Data Shape:", data.shape)

# -------------------------------
# FEATURES
# -------------------------------
features = [
    "packet_size","src_port","dst_port","protocol",
    "tcp_len","tcp_window","time_delta"
]

X = data[features]
y = data["label"]

# -------------------------------
# SCALE
# -------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -------------------------------
# SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

# -------------------------------
# MODEL
# -------------------------------
model = XGBClassifier(
    n_estimators=150,
    max_depth=5,
    learning_rate=0.1,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# -------------------------------
# EVALUATION
# -------------------------------
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_prob))

# -------------------------------
# SAVE MODEL
# -------------------------------
pickle.dump(model, open(os.path.join(BASE_DIR, "model.pkl"), "wb"))
pickle.dump(scaler, open(os.path.join(BASE_DIR, "scaler.pkl"), "wb"))

print("\nModel saved successfully!")
