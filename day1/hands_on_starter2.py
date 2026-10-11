from datetime import datetime
import random
import time
import csv
import os

LOG_FILE = "day1_log.txt"
CSV_FILE = "day1_sensor_data.csv"


# STEP 1 — Generate sensor data
def generate_sensor_data():
    return {
        "temperature": round(random.uniform(50, 95), 2),
        "pressure": round(random.uniform(1.0, 10.0), 2),
        "vibration": round(random.uniform(0.1, 5.0), 2),
        "current": round(random.uniform(1.0, 20.0), 2),
        "rpm": random.randint(500, 3500)
    }


# STEP 2 — Automation rules
RULES = [
    {
        "name": "HIGH_TEMP",
        "priority": 1,
        "condition": lambda r: r["temperature"] > 90,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 2,
        "condition": lambda r: r["pressure"] > 8,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 2,
        "condition": lambda r: r["current"] > 15,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_RPM",
        "priority": 2,
        "condition": lambda r: r["rpm"] > 3200,
        "action": "REDUCE_RPM"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 3,
        "condition": lambda r: r["vibration"] > 4,
        "action": "INSPECT_MACHINE"
    },
    {
        "name": "LOW_TEMP",
        "priority": 4,
        "condition": lambda r: r["temperature"] < 50,
        "action": "CHECK_TEMPERATURE"
    },
    {
        "name": "LOW_PRESSURE",
        "priority": 5,
        "condition": lambda r: r["pressure"] < 2,
        "action": "CHECK_PRESSURE"
    },
    {
        "name": "LOW_VIBRATION",
        "priority": 6,
        "condition": lambda r: r["vibration"] < 0.1,
        "action": "CHECK_VIBRATION"
    },
    {
        "name": "LOW_CURRENT",
        "priority": 6,
        "condition": lambda r: r["current"] < 1.0,
        "action": "CHECK_CURRENT"
    },
    {
        "name": "LOW_RPM",
        "priority": 6,
        "condition": lambda r: r["rpm"] < 800,
        "action": "CHECK_MOTOR"
    }
]


# STEP 3 — Evaluate rules
def evaluate_rules(reading, rules):
    rules = sorted(rules, key=lambda r: r["priority"])

    for rule in rules:
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# STEP 4 — Execute action
def take_action(action):
    actions = {
        "STOP_MACHINE": "Machine stopped due to a critical reading.",
        "REDUCE_RPM": "RPM too high. Reduce machine speed.",
        "CHECK_TEMPERATURE": "Check the temperature sensor.",
        "CHECK_PRESSURE": "Inspect the pressure system.",
        "INSPECT_MACHINE": "High vibration. Inspect the machine.",
        "CHECK_VIBRATION": "Check the vibration sensor.",
        "CHECK_CURRENT": "Check motor current and power supply.",
        "CHECK_MOTOR": "RPM too low. Inspect the motor.",
        "CONTINUE_NORMAL": "All readings normal. Machine continues running."
    }
    return actions.get(action, f"No handler for action: {action}")


# STEP 5 — Log decisions
def log_decision(reading, rule_name, action):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"{datetime.now().isoformat(timespec='seconds')} | "
            f"Reading: {reading} | Rule: {rule_name} | "
            f"Action: {action}\n"
        )


# STEP 6 — Save sensor data as CSV for ML
def save_csv(reading, rule_name):
    file_exists = os.path.exists(CSV_FILE)

    # State label for supervised ML training
    state = (
        "NORMAL" if rule_name == "NO_RULE_FIRED"
        else rule_name
    )

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "temperature", "pressure", "vibration",
                "current", "rpm", "state"
            ]
        )

        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writeheader()

        writer.writerow({**reading, "state": state})


def main():
    for tick in range(1, 250):
        reading = generate_sensor_data()
        rule_name, action = evaluate_rules(reading, RULES)
        outcome = take_action(action)

        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           THINK -> {rule_name}")
        print(f"           ACT   -> {outcome}\n")

        log_decision(reading, rule_name, action)
        save_csv(reading, rule_name)

        time.sleep(0.2)


if __name__ == "__main__":
    main()
