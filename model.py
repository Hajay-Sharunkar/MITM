import pandas as pd
import pickle

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# -----------------------------
# 1. LOAD DATA
# -----------------------------
data = pd.read_csv("final_dataset.csv")

print("Columns:", data.columns)

# -----------------------------
# 2. BALANCE DATASET
# -----------------------------
attack = data[data['label'] == 1]
normal = data[data['label'] == 0]

min_size = min(len(attack), len(normal))

attack = attack.sample(min_size, random_state=42)
normal = normal.sample(min_size, random_state=42)

data = pd.concat([attack, normal])

print("\nBalanced dataset:")
print(data['label'].value_counts())

# -----------------------------
# 3. SELECT FEATURES
# -----------------------------
X = data[['packet_size','src_port','dst_port','protocol']]
y = data['label']

# -----------------------------
# 4. SCALE FEATURES
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 5. TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 6. TRAIN MODEL (Random Forest)
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# 7. PREDICT
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# 8. EVALUATION
# -----------------------------
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nAccuracy:", accuracy_score(y_test, y_pred))

# -----------------------------
# 9. CROSS VALIDATION
# -----------------------------
scores = cross_val_score(model, X_scaled, y, cv=5)
print("\nCross-validation Accuracy:", scores.mean())

# -----------------------------
# 10. SAVE MODEL + SCALER
# -----------------------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("\nModel saved as model.pkl")
print("Scaler saved as scaler.pkl")
