import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = "data/historical_wear_data.csv"
MODEL_PATH = "wear_model.pkl"

FEATURES = [
    "shoulder_torque", "shoulder_temp", "shoulder_vibration",
    "elbow_torque", "elbow_temp", "elbow_vibration",
    "wrist_torque", "wrist_temp", "wrist_vibration"
]

def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df["wear_status"].str.strip().str.lower()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("Wear Prediction Model Accuracy:", accuracy_score(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    print("Saved model to", MODEL_PATH)

if __name__ == "__main__":
    train_model()
