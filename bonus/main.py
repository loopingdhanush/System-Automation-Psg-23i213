import os
import joblib
import pandas as pd

MODEL_PATH = "wear_model.pkl"
LOG_PATH = "data/maintenance_log.txt"

FEATURES = [
    "shoulder_torque", "shoulder_temp", "shoulder_vibration",
    "elbow_torque", "elbow_temp", "elbow_vibration",
    "wrist_torque", "wrist_temp", "wrist_vibration"
]


# 1. Immediate Safety Stop Check (Deterministic, no ML model)
def check_immediate_stop(sensor):
    # Temperature hard limit: 85 C
    for joint in ["shoulder", "elbow", "wrist"]:
        if sensor[f"{joint}_temp"] > 85.0:
            return True, f"{joint} temperature {sensor[f'{joint}_temp']}C exceeds safety limit (85C)"

    # Vibration hard limit: 7.0 mm/s
    for joint in ["shoulder", "elbow", "wrist"]:
        if sensor[f"{joint}_vibration"] > 7.0:
            return True, f"{joint} vibration {sensor[f'{joint}_vibration']} mm/s exceeds safety limit (7.0 mm/s)"

    # Torque mechanical limits
    if sensor["shoulder_torque"] > 160.0:
        return True, f"shoulder torque {sensor['shoulder_torque']} Nm exceeds limit (160 Nm)"
    if sensor["elbow_torque"] > 140.0:
        return True, f"elbow torque {sensor['elbow_torque']} Nm exceeds limit (140 Nm)"
    if sensor["wrist_torque"] > 80.0:
        return True, f"wrist torque {sensor['wrist_torque']} Nm exceeds limit (80 Nm)"

    return False, "ok"


# 2. Spoofed Sensor Defense
# Someone might report low torque to hide joint binding/friction
def check_spoofed_sensor(sensor):
    for joint in ["shoulder", "elbow", "wrist"]:
        t = sensor[f"{joint}_temp"]
        v = sensor[f"{joint}_vibration"]
        trq = sensor[f"{joint}_torque"]

        # If temperature and vibration are high, torque cannot be low or zero
        if t >= 75.0 and v >= 4.5 and trq <= 35.0:
            return True, f"Spoofed {joint} sensor: reported torque {trq} Nm is too low for temp {t}C and vibration {v}"

        if trq <= 0.0 and (v > 2.0 or t > 55.0):
            return True, f"Spoofed {joint} sensor: non-positive torque {trq} Nm while joint is running"

    return False, "ok"


# 3. Technician Maintenance Log Analysis
def read_maintenance_notes(arm_id):
    if not os.path.exists(LOG_PATH):
        return "none", "No log file found"

    relevant_lines = []
    with open(LOG_PATH, "r") as f:
        for line in f:
            if arm_id.upper() in line.upper():
                relevant_lines.append(line.strip())

    if not relevant_lines:
        return "none", "No notes for this arm"

    full_text = " ".join(relevant_lines).lower()

    # Check for critical keywords
    critical_words = ["grinding", "burning", "stiff", "metal dust", "broken"]
    for word in critical_words:
        if word in full_text:
            return "critical", relevant_lines

    # Check for warning keywords
    warning_words = ["buzzing", "noise", "vibration", "warm"]
    for word in warning_words:
        if word in full_text:
            return "warning", relevant_lines

    return "normal", relevant_lines


# 4. Predict Wear using ML Model
def predict_wear(sensor, model):
    df = pd.DataFrame([sensor], columns=FEATURES)
    pred = model.predict(df)[0]
    return pred


# 5. Final Decision Logic for one arm
def evaluate_arm(arm_id, sensor, model):
    # Rule 1: Immediate safety stop has highest priority
    stopped, reason = check_immediate_stop(sensor)
    if stopped:
        return {
            "decision": "EMERGENCY_STOP",
            "reason": f"Immediate safety threshold breached: {reason}",
            "wear_prediction": "bypassed",
            "notes_signal": "bypassed"
        }

    # Rule 2: Spoof defense
    spoofed, spoof_reason = check_spoofed_sensor(sensor)
    if spoofed:
        return {
            "decision": "EMERGENCY_STOP",
            "reason": f"Sensor attack detected: {spoof_reason}",
            "wear_prediction": "bypassed",
            "notes_signal": "bypassed"
        }

    # Rule 3 & 4: Model prediction and maintenance notes
    wear = predict_wear(sensor, model)
    note_status, note_lines = read_maintenance_notes(arm_id)

    # Combine both signals
    if wear == "severe" or note_status == "critical":
        decision = "SCHEDULE_MAINTENANCE"
        reason = f"Wear: {wear}, Technician Note: {note_status}"
    elif wear == "moderate" or note_status == "warning":
        decision = "MONITOR"
        reason = f"Wear: {wear}, Technician Note: {note_status}"
    else:
        decision = "SAFE"
        reason = f"Wear: {wear}, Technician Note: {note_status}"

    return {
        "decision": decision,
        "reason": reason,
        "wear_prediction": wear,
        "notes_signal": note_status
    }


def main():
    print("Loading wear model...")
    model = joblib.load(MODEL_PATH)

    # Test cases showing each reachable decision
    fleet = [
        {
            "arm_id": "ARM_01",
            "info": "Healthy arm, routine maintenance",
            "sensor": {
                "shoulder_torque": 50.0, "shoulder_temp": 42.0, "shoulder_vibration": 1.1,
                "elbow_torque": 40.0, "elbow_temp": 40.0, "elbow_vibration": 1.0,
                "wrist_torque": 20.0, "wrist_temp": 35.0, "wrist_vibration": 0.8
            }
        },
        {
            "arm_id": "ARM_02",
            "info": "Minor wrist buzzing noted by technician",
            "sensor": {
                "shoulder_torque": 80.0, "shoulder_temp": 60.0, "shoulder_vibration": 2.5,
                "elbow_torque": 70.0, "elbow_temp": 58.0, "elbow_vibration": 2.4,
                "wrist_torque": 40.0, "wrist_temp": 55.0, "wrist_vibration": 2.2
            }
        },
        {
            "arm_id": "ARM_03",
            "info": "High wear with grinding sound reported",
            "sensor": {
                "shoulder_torque": 120.0, "shoulder_temp": 75.0, "shoulder_vibration": 5.0,
                "elbow_torque": 110.0, "elbow_temp": 74.0, "elbow_vibration": 5.2,
                "wrist_torque": 60.0, "wrist_temp": 70.0, "wrist_vibration": 4.5
            }
        },
        {
            "arm_id": "ARM_04",
            "info": "Dangerous overheating on shoulder joint",
            "sensor": {
                "shoulder_torque": 130.0, "shoulder_temp": 89.0, "shoulder_vibration": 5.8,
                "elbow_torque": 105.0, "elbow_temp": 79.0, "elbow_vibration": 5.1,
                "wrist_torque": 58.0, "wrist_temp": 72.0, "wrist_vibration": 4.8
            }
        },
        {
            "arm_id": "ARM_05",
            "info": "Spoofed torque attack (hot and vibrating, but reports 15 Nm)",
            "sensor": {
                "shoulder_torque": 15.0, "shoulder_temp": 78.0, "shoulder_vibration": 5.2,
                "elbow_torque": 45.0, "elbow_temp": 48.0, "elbow_vibration": 1.4,
                "wrist_torque": 22.0, "wrist_temp": 38.0, "wrist_vibration": 0.9
            }
        }
    ]

    print("\n--- Fleet Health Evaluation ---")
    for item in fleet:
        res = evaluate_arm(item["arm_id"], item["sensor"], model)
        print(f"\nArm: {item['arm_id']} ({item['info']})")
        print(f"  Decision   : {res['decision']}")
        print(f"  Reason     : {res['reason']}")
        print(f"  Model Wear : {res['wear_prediction']}")
        print(f"  Notes      : {res['notes_signal']}")

if __name__ == "__main__":
    main()
