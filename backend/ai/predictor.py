import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# ================= PATH =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "hospital_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# create models folder if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

DISEASE_MODEL_PATH = os.path.join(MODEL_DIR, "disease_model.pkl")
ICU_MODEL_PATH = os.path.join(MODEL_DIR, "icu_model.pkl")

# ================= LOAD DATA =================
print("📊 Loading dataset...")

# FIX: handle comma OR tab file
try:
    df = pd.read_csv(DATA_PATH)
    if len(df.columns) == 1:
        df = pd.read_csv(DATA_PATH, sep="\t")
except Exception as e:
    raise ValueError(f"❌ Error loading dataset: {e}")

print("✅ Dataset loaded:", df.shape)
print("Columns:", df.columns.tolist())

# ================= FIX COLUMN =================
if 'sugar' not in df.columns:
    if 'glucose' in df.columns:
        df.rename(columns={'glucose': 'sugar'}, inplace=True)
        print("🔁 Renamed 'glucose' → 'sugar'")
    else:
        raise ValueError("❌ Missing sugar/glucose column")

# ================= CLEAN DATA =================
print("🧹 Cleaning dataset...")

numeric_cols = ['age', 'bp', 'sugar', 'heart_rate', 'spo2']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].fillna(df[col].median())

df['disease'] = df['disease'].fillna("Unknown")
df['icu'] = df['icu'].fillna(0)

print("✅ Missing values handled")

# ================= FEATURES =================
X = df[['age', 'bp', 'sugar', 'heart_rate', 'spo2']]
y_disease = df['disease']
y_icu = df['icu']

# ================= SPLIT =================
X_train, X_test, y_d_train, y_d_test = train_test_split(
    X, y_disease, test_size=0.2, random_state=42
)

X_train2, X_test2, y_i_train, y_i_test = train_test_split(
    X, y_icu, test_size=0.2, random_state=42
)

# ================= TRAIN =================
print("🧠 Training models...")

disease_model = RandomForestClassifier(n_estimators=100)
icu_model = RandomForestClassifier(n_estimators=100)

disease_model.fit(X_train, y_d_train)
icu_model.fit(X_train2, y_i_train)

# ================= SAVE =================
joblib.dump(disease_model, DISEASE_MODEL_PATH)
joblib.dump(icu_model, ICU_MODEL_PATH)

print("✅ Models saved:")
print(" -", DISEASE_MODEL_PATH)
print(" -", ICU_MODEL_PATH)

# ================= LOAD MODELS =================
disease_model = joblib.load(DISEASE_MODEL_PATH)
icu_model = joblib.load(ICU_MODEL_PATH)

# ================= AI FUNCTIONS =================

def predict_disease(age, bp, sugar, heart_rate, spo2):
    data = pd.DataFrame([[age, bp, sugar, heart_rate, spo2]],
                        columns=['age', 'bp', 'sugar', 'heart_rate', 'spo2'])
    return str(disease_model.predict(data)[0])


def predict_icu(age, bp, sugar, heart_rate, spo2):
    data = pd.DataFrame([[age, bp, sugar, heart_rate, spo2]],
                        columns=['age', 'bp', 'sugar', 'heart_rate', 'spo2'])

    pred = int(icu_model.predict(data)[0])
    prob = float(icu_model.predict_proba(data)[0][1]) * 100

    return {
        "icu": pred,
        "probability": round(prob, 2)
    }


def risk_score(age, bp, sugar, heart_rate, spo2):
    icu_data = predict_icu(age, bp, sugar, heart_rate, spo2)

    score = (
        (bp / 180) * 20 +
        (sugar / 250) * 20 +
        (heart_rate / 150) * 20 +
        ((100 - spo2) / 100) * 20 +
        (age / 100) * 20
    )

    return {
        "risk_score": round(score, 2),
        "risk_level": (
            "HIGH" if score > 70 else
            "MEDIUM" if score > 40 else
            "LOW"
        ),
        "icu_probability": icu_data["probability"]
    }


# ================= APPOINTMENT PREDICTION =================

def predict_appointments(month):
    import random

    base = 100

    if month in [11, 12, 1]:
        base += 40
    elif month in [4, 5]:
        base += 20
    else:
        base += 10

    prediction = base + random.randint(-15, 15)

    return {
        "month": month,
        "predicted_appointments": prediction
    }


# ================= SIMPLE CHATBOT =================

def chatbot(message: str):
    message = message.lower()

    if "fever" in message:
        return "You may have an infection. Please consult a doctor."
    elif "headache" in message:
        return "Stay hydrated and rest. If severe, see a doctor."
    elif "hello" in message:
        return "Hello! How can I help you?"
    else:
        return "Please consult a doctor for proper diagnosis."


# ================= TEST =================
print("\n🔍 Testing prediction...")

sample = [60, 170, 220, 100, 90]

print("Disease Prediction:", predict_disease(*sample))
print("ICU Prediction:", predict_icu(*sample))
print("Risk Score:", risk_score(*sample))
