import joblib
import time
from datetime import datetime

MODEL_PATH = "./sensor_model.pkl"
LOG_FILE = "./decision_log.txt"

model = joblib.load(MODEL_PATH)

def predict_state(reading):
    features = [
        "temperature", "pressure", "vibration", "rpm", "current"
    ]

    X = pd.DataFrame([reading], columns=features)
    return model.predict(X)[0]


def take_action(action):
    actions = {
        "normal": "All readings are normal. Machine continues running.",
        "warning": "Abnormal reading detected. Schedule machine inspection.",
        "critical": "Critical condition detected. Stop machine and alert operator."
    }
    return actions.get(action, f"No handler yet for action: {action}")


def log_decision(reading, prediction, action):
    with open(LOG_FILE, "a") as file:
        file.write(
            f"{datetime.now().isoformat(timespec='seconds')} | "
            f"Reading: {reading} | "
            f"Prediction: {prediction} | "
            f"Action: {action}\n"
        )


def main():
    for tick in range(1, 11):
        reading = generate_sensor_data()

        prediction = predict_state(reading)
        outcome = take_action(prediction)

        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           PREDICT -> {prediction}")
        print(f"           ACT     -> {outcome}\n")

        log_decision(reading, prediction, outcome)
        time.sleep(0.2)


if __name__ == "__main__":
    main()