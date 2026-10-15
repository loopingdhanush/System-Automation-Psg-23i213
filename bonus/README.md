# Bonus: Robotic Arm Joint Health Monitoring System

This folder contains the bonus challenge implementation for joint health monitoring of 6-axis robotic arms.

## Files
- `data/historical_wear_data.csv`: Synthetic dataset with 80 labeled sensor readings (normal, moderate, severe).
- `data/maintenance_log.txt`: Sample technician inspection notes (10 entries with relevant and facility notes).
- `generate_data.py`: Generates the dataset and sample maintenance log.
- `train_model.py`: Trains a Decision Tree model to predict wear from joint sensors.
- `main.py`: Main script running the health monitoring pipeline and testing all 4 decisions.
- `EXPLANATION.md`: Written explanation covering thresholds, fusion logic, and spoof defense.

## How to Run

1. Generate the data:
```bash
python generate_data.py
```

2. Train the model:
```bash
python train_model.py
```

3. Run the system demo:
```bash
python main.py
```
