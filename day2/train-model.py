
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = Path(__file__).parent/"data"/"day1_sensor_data.csv"
MODEL_PATH = "./sensor_model.pkl"

FEATURES = [
    "temperature", "pressure", "vibration", "rpm", "current"
]


def train_model():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df["state"].str.strip().str.lower()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
    )

    model = DecisionTreeClassifier(
        max_depth=4,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    print("Model saved to", MODEL_PATH)

    return model


if __name__ == "__main__":
    train_model()
