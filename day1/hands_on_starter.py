""" DAY 1 · HANDS-ON — Build Your Rule Engine
23IF02 System Automation

Work through the TODOs in order. Each one matches a step on the
"Hands-on · Build Your Rule Engine" slide. Run this file after each
step to see your progress:

python hands_on_starter.py

Need the answer? See hands_on_solution.py — but try it yourself first.
"""
from datetime import datetime
import random
import time

LOG_FILE = "day1_log.txt"

# ---------------------------------------------------------------------------
# STEP 1 — Generate simulated sensor data
# ---------------------------------------------------------------------------
def generate_sensor_data():
    """Return a dict with at least 'temperature', 'pressure', 'vibration'."""
    # TODO: fill in realistic random values, e.g. temperature 50-95 (deg C)
    return {
        "temperature": round(random.uniform(50, 95), 2),  # °C
        "pressure": round(random.uniform(1.0, 10.0), 2),  # bar
        "vibration": round(random.uniform(0.1, 5.0), 2),  # mm/s
        "current": round(random.uniform(1.0, 20.0), 2)    # Amperes (A)
    }
    # STRETCH GOAL (after the 8 steps below all work): real sensors aren't
    # perfectly clean. Try making one field randomly return None (a
    # dropout) or spike far outside its normal range every so often, then
    # update evaluate_rules() so a dropout doesn't crash your engine.


# ---------------------------------------------------------------------------
# STEP 2 — Write your first automation rules
# STEP 7 — Add a rule of your own (add another dict to this list)
# STEP 8 — Add one priority rule (lower "priority" number checked first)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# STEP 3 — Detect machine state from the rules
# ---------------------------------------------------------------------------
def evaluate_rules(reading, rules):
    """Return the first matching rule based on priority."""
    rules = sorted(rules, key=lambda r: r["priority"])

    for rule in rules:
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# ---------------------------------------------------------------------------
# STEP 4 — Trigger an action when a rule fires
# ---------------------------------------------------------------------------
def take_action(action):
    """Return a human-readable string describing what happens for this action."""
    actions = {
        "STOP_MACHINE": "Machine stopped due to a critical reading.",
        "CHECK_TEMPERATURE": "Temperature is too low. Check the sensor.",
        "CHECK_PRESSURE": "Pressure is abnormal. Inspect the pressure system.",
        "INSPECT_MACHINE": "High vibration detected. Inspect the machine.",
        "CHECK_VIBRATION": "Vibration is too low. Check the sensor.",
        "CONTINUE_NORMAL": "All readings are normal. Machine continues running.",
        "CHECK_CURRENT": "Current is too low. Check the motor and power supply.",
        "CONTINUE_NORMAL": "All readings are normal. Machine continues running."
    }
    return actions.get(action, f"no handler yet for action: {action}")
  


# ---------------------------------------------------------------------------
# STEP 5 — Log every decision made
# ---------------------------------------------------------------------------

def log_decision(reading, rule_name, action):
    """Append one line to LOG_FILE with the reading, rule fired, and action."""
    # TODO: open(LOG_FILE, "a") and write a line
    with open(LOG_FILE, "a") as file:
        file.write(
            f"{datetime.now().isoformat(timespec='seconds')} | "
            f"Reading: {reading} | "
            f"Rule: {rule_name} | "
            f"Action: {action}\n"
        )

# ---------------------------------------------------------------------------
# STEP 6 — Add a second sensor to the system
# TODO: add e.g. "current" to generate_sensor_data(), then use it in a rule
# ---------------------------------------------------------------------------


def main():
    for tick in range(1, 11):
        reading = generate_sensor_data()
        rule_name, action = evaluate_rules(reading, RULES)
        outcome = take_action(action)

        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           THINK -> {rule_name}")
        print(f"           ACT   -> {outcome}\n")

        log_decision(reading, rule_name, action)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
