import random
import csv
import os

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

# 1. Generate Historical Joint Sensor Dataset (at least 50 readings)
# 6-axis arm joints: shoulder, elbow, wrist
# Metrics: torque (Nm), temp (C), vibration (mm/s)

data_file = "data/historical_wear_data.csv"

rows = []
for i in range(80):
    # 3 classes: normal, moderate, severe
    if i < 35:
        wear = "normal"
        s_trq = round(random.uniform(40, 70), 1)
        s_tmp = round(random.uniform(35, 55), 1)
        s_vib = round(random.uniform(0.5, 2.0), 1)

        e_trq = round(random.uniform(30, 60), 1)
        e_tmp = round(random.uniform(35, 55), 1)
        e_vib = round(random.uniform(0.5, 2.0), 1)

        w_trq = round(random.uniform(15, 35), 1)
        w_tmp = round(random.uniform(30, 50), 1)
        w_vib = round(random.uniform(0.4, 1.8), 1)

    elif i < 60:
        wear = "moderate"
        s_trq = round(random.uniform(75, 105), 1)
        s_tmp = round(random.uniform(55, 70), 1)
        s_vib = round(random.uniform(2.1, 4.0), 1)

        e_trq = round(random.uniform(65, 90), 1)
        e_tmp = round(random.uniform(55, 68), 1)
        e_vib = round(random.uniform(2.1, 4.0), 1)

        w_trq = round(random.uniform(35, 55), 1)
        w_tmp = round(random.uniform(50, 65), 1)
        w_vib = round(random.uniform(1.8, 3.5), 1)

    else:
        wear = "severe"
        s_trq = round(random.uniform(110, 150), 1)
        s_tmp = round(random.uniform(70, 83), 1)
        s_vib = round(random.uniform(4.2, 6.5), 1)

        e_trq = round(random.uniform(95, 130), 1)
        e_tmp = round(random.uniform(68, 82), 1)
        e_vib = round(random.uniform(4.2, 6.5), 1)

        w_trq = round(random.uniform(55, 75), 1)
        w_tmp = round(random.uniform(65, 80), 1)
        w_vib = round(random.uniform(3.8, 6.2), 1)

    rows.append([
        s_trq, s_tmp, s_vib,
        e_trq, e_tmp, e_vib,
        w_trq, w_tmp, w_vib,
        wear
    ])

with open(data_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "shoulder_torque", "shoulder_temp", "shoulder_vibration",
        "elbow_torque", "elbow_temp", "elbow_vibration",
        "wrist_torque", "wrist_temp", "wrist_vibration",
        "wear_status"
    ])
    writer.writerows(rows)

print(f"Dataset generated: {len(rows)} samples saved to {data_file}")


# 2. Generate Technician Maintenance Log (at least 8 entries, mixing relevant and irrelevant)
log_file = "data/maintenance_log.txt"

notes = [
    "ARM_01: Monthly inspection done, all joints moving smooth and no issues found.",
    "FACILITY: Replaced water filter on cell B cooling unit.",
    "ARM_02: Technician heard minor buzzing sound from wrist joint during high speed run.",
    "SUPPLIES: 10 tubes of joint grease restocked in cabinet.",
    "ARM_03: Elbow joint has loud grinding noise and feels stiff when extending.",
    "WORKSHOP: Cleaned metal shavings off floor near work area.",
    "ARM_04: High heat and burning smell coming from shoulder motor housing.",
    "CALIBRATION: Tool height sensor checked and zeroed.",
    "ARM_01: Routine joint lube applied, arm running quiet.",
    "ARM_03: Metal dust noticed near elbow gearbox gear teeth."
]

with open(log_file, "w") as f:
    for n in notes:
        f.write(n + "\n")

print(f"Log generated: {len(notes)} entries saved to {log_file}")
