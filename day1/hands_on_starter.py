
import csv
import random

filename = "factory_sensor_data.csv"

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(40, 100), 2),
        "pressure": round(random.uniform(1.0, 12.0), 2),
        "vibration": round(random.uniform(0.0, 6.0), 2),
        "rpm": random.randint(500, 3500),
        "current": round(random.uniform(0.5, 25.0), 2)
    }

def get_state(r):
    # Critical: high readings
    if (
        r["temperature"] > 90
        or r["pressure"] > 8
        or r["vibration"] > 4
        or r["rpm"] > 3000
        or r["current"] > 15
    ):
        return "critical"

    # Warning: low readings
    if (
        r["temperature"] < 50
        or r["pressure"] < 2
        or r["vibration"] < 0.1
        or r["rpm"] < 800
        or r["current"] < 1.0
    ):
        return "warning"

    return "normal"

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "temperature",
        "pressure",
        "vibration",
        "rpm",
        "current",
        "state"
    ])

    for _ in range(250):
        sensor = generate_sensor_data()
        state = get_state(sensor)

        writer.writerow([
            sensor["temperature"],
            sensor["pressure"],
            sensor["vibration"],
            sensor["rpm"],
            sensor["current"],
            state
        ])

print(f"Generated {filename} with 250 records.")
