
import pandas as pd
import joblib
import random
import time

from datetime import datetime

MODEL_PATH = "./sensor_model.pkl"
LOG_FILE = "./decision_log.txt"

FEATURES = [
    "temperature",
    "pressure",
    "vibration",
    "rpm",
    "current"
]

model = joblib.load(MODEL_PATH)


RULES = [
    {
        "name": "HIGH_TEMP",
        "priority": 1,
        "condition": lambda r: r["temperature"] > 90,
        "action": "STOP_MACHINE"
    },
    {
        "name": "LOW_TEMP",
        "priority": 4,
        "condition": lambda r: r["temperature"] < 50,
        "action": "CHECK_TEMPERATURE"
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 2,
        "condition": lambda r: r["pressure"] > 8,
        "action": "STOP_MACHINE"
    },
    {
        "name": "LOW_PRESSURE",
        "priority": 5,
        "condition": lambda r: r["pressure"] < 2,
        "action": "CHECK_PRESSURE"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 3,
        "condition": lambda r: r["vibration"] > 4,
        "action": "INSPECT_MACHINE"
    },
    {
        "name": "LOW_VIBRATION",
        "priority": 6,
        "condition": lambda r: r["vibration"] < 0.1,
        "action": "CHECK_VIBRATION"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 2,
        "condition": lambda r: r["current"] > 15,
        "action": "STOP_MACHINE"
    },
    {
        "name": "LOW_CURRENT",
        "priority": 5,
        "condition": lambda r: r["current"] < 1.0,
        "action": "CHECK_CURRENT"
    }
]


def generate_sensor_data():
    return {
        "temperature": round(random.uniform(40, 100), 2),
        "pressure": round(random.uniform(1, 12), 2),
        "vibration": round(random.uniform(0, 6), 2),
        "rpm": random.randint(500, 3500),
        "current": round(random.uniform(0.5, 25), 2)
    }


def predict_state(reading):
    X = pd.DataFrame([reading], columns=FEATURES)
    return str(model.predict(X)[0]).strip().lower()


def evaluate_rules(reading):
    matched_rules = [
        rule for rule in RULES
        if rule["condition"](reading)
    ]

    matched_rules.sort(key=lambda rule: rule["priority"])

    return matched_rules


def take_action(action):
    actions = {
        "normal": (
            "All readings are normal. Machine continues running."
        ),
        "warning": (
            "Abnormal reading detected. Schedule machine inspection."
        ),
        "critical": (
            "Critical condition detected. Stop machine and alert operator."
        ),
        "overheating": (
            "OVERHEATING! Check the cooling system and alert the operator."
        ),
        "high_temp": (
            "HIGH TEMPERATURE! Inspect cooling, ventilation, and temperature sensors."
        ),
        "high_pressure": (
            "HIGH PRESSURE! Inspect valves, pressure regulators, and sensors."
        ),
        "low_pressure": (
            "LOW PRESSURE! Check for leaks and inspect pump performance."
        ),
        "motor_overload": (
            "MOTOR OVERLOAD! Check current draw, mechanical load, and blockages."
        ),
        "high_vibration": (
            "HIGH VIBRATION! Inspect bearings, shaft alignment, and mounting bolts."
        ),
        "low_vibration": (
            "LOW VIBRATION! Check the vibration sensor and machine operation."
        ),
        "high_current": (
            "HIGH CURRENT! Inspect electrical connections and motor load."
        ),
        "low_current": (
            "LOW CURRENT! Check the power supply, motor connections, and sensor."
        ),
        "high_rpm": (
            "HIGH RPM! Check the speed controller and permitted operating speed."
        ),
        "low_rpm": (
            "LOW RPM! Check motor performance, power supply, and mechanical load."
        )
    }

    return actions.get(
        str(action).strip().lower(),
        f"Unknown action: {action}. Alert the operator for inspection."
    )


def hybrid_decision(reading):
    prediction = predict_state(reading) # ml prediction
    matched_rules = evaluate_rules(reading) # rules

    if matched_rules:
        selected_rule = matched_rules[0]

        rule_actions = {
            "STOP_MACHINE": (
                "STOP MACHINE! A safety threshold has been exceeded. "
                "Alert the operator."
            ),
            "CHECK_TEMPERATURE": (
                "Check temperature readings and inspect the machine."
            ),
            "CHECK_PRESSURE": (
                "Check pressure readings, pumps, and possible leaks."
            ),
            "INSPECT_MACHINE": (
                "Inspect bearings, alignment, mounting, and rotating components."
            ),
            "CHECK_VIBRATION": (
                "Check the vibration sensor and machine condition."
            ),
            "CHECK_CURRENT": (
                "Check the current sensor, power supply, and motor connections."
            )
        }

        outcome = rule_actions.get(
            selected_rule["action"],
            "Unknown rule action. Alert the operator."
        )

        return {
            "prediction": prediction,
            "rule": selected_rule["name"],
            "matched_rules": [
                rule["name"] for rule in matched_rules
            ],
            "action": selected_rule["action"],
            "outcome": outcome,
            "reason": (
                f"Rule {selected_rule['name']} triggered "
                f"(priority {selected_rule['priority']})"
            )
        }

    outcome = take_action(prediction)

    return {
        "prediction": prediction,
        "rule": "NONE",
        "matched_rules": [],
        "action": prediction.upper(),
        "outcome": outcome,
        "reason": "No rule triggered; action based on ML prediction"
    }


def log_decision(reading, result):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now().isoformat(timespec='seconds')} | "
            f"Reading: {reading} | "
            f"ML Prediction: {result['prediction']} | "
            f"Matched Rules: {result['matched_rules']} | "
            f"Selected Rule: {result['rule']} | "
            f"Action: {result['action']} | "
            f"Reason: {result['reason']}\n"
        )


def main():
    for tick in range(1, 11):
        reading = generate_sensor_data()

        result = hybrid_decision(reading)

        print(f"[Tick {tick:02d}] SENSE   -> {reading}")
        print(f"           ML      -> {result['prediction']}")
        print(f"           RULE    -> {result['rule']}")
        print(f"           MATCHED -> {result['matched_rules']}")
        print(f"           ACT     -> {result['action']}")
        print(f"           OUTCOME -> {result['outcome']}")
        print(f"           REASON  -> {result['reason']}\n")

        log_decision(reading, result)

        time.sleep(0.2)


if __name__ == "__main__":
    main()
