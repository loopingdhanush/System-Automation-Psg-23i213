# Robotic Arm Joint Health Monitoring System - Project Explanation

### 1. Safety Thresholds for the Immediate-Stop Check
The immediate safety check is deterministic and uses simple rule-based thresholds on raw sensor inputs. It does not use the machine learning model, so even if the model fails or takes time to process, the system can stop the arm instantly.

The thresholds were chosen based on standard physical limits for 6-axis industrial arms:
- **Temperature (> 85°C):** Motor windings and joint lubricants start to break down and degrade rapidly once temperature crosses 80–90°C. Going above 85°C risks burning out the motor coil or causing thermal damage.
- **Vibration (> 7.0 mm/s):** Under normal running conditions, joint vibration is usually between 0.5 to 2.5 mm/s. A reading over 7.0 mm/s means there is mechanical damage such as broken gear teeth or failing joint bearings.
- **Torque (Shoulder > 160 Nm, Elbow > 140 Nm, Wrist > 80 Nm):** The shoulder carries the heaviest load, while the wrist carries the lightest. Setting these limits around 120-130% of normal maximum rated load catches sudden mechanical jams or physical collisions before the gears or motor shafts snap.

---

### 2. Combining Model Prediction and Maintenance Notes
The final decision uses two separate signals: numeric sensor data processed by a Decision Tree classifier, and text logs written by technicians during inspections.

1. **Model Prediction:** The model looks at current torque, temperature, and vibration across all three joints and predicts the wear state as `normal`, `moderate`, or `severe`.
2. **Maintenance Log:** Technicians write simple inspection sentences in `maintenance_log.txt`. The code checks if the arm ID appears in any line and looks for key phrases:
   - Critical terms like "grinding", "burning", "stiff", or "metal dust" give a `critical` signal.
   - Warning terms like "buzzing", "noise", "vibration", or "warm" give a `warning` signal.
   - Unrelated entries (such as tool calibration or workshop cleaning) do not match the arm ID and are ignored.

**Combination Logic:**
- If an immediate safety threshold is breached or a spoof attack is detected, the arm gets `EMERGENCY_STOP`.
- If the model predicts `severe` wear OR the technician note is `critical`, the arm gets `SCHEDULE_MAINTENANCE`.
- If the model predicts `moderate` wear OR the technician note is `warning`, the arm gets `MONITOR`.
- If the model predicts `normal` wear AND technician notes are clean, the arm gets `SAFE`.

This allows human observations (like hearing grinding or smelling burning grease) to escalate maintenance even if the numerical sensor reading has not crossed hard limits yet.

---

### 3. Spoofed-Sensor Defense
**How it works:**
In an electric robotic arm, torque, temperature, and vibration are physically related. When a joint is struggling, binding, or experiencing high friction, it heats up and vibrates heavily. 
If an attacker manipulates the sensor to send a fake "safe" torque reading (for example, reporting 15 Nm instead of high torque) to hide a problem, the system compares torque with temperature and vibration. If temperature is over 75°C and vibration is over 4.5 mm/s, but reported torque is under 35 Nm (or negative/zero), this is physically impossible during normal operation. The system flags this inconsistency as a spoofed sensor and stops the arm.

**What it catches:**
- Low-torque masking attacks where someone reports false low torque to avoid overload warnings.
- Frozen or stuck sensor values where a dead sensor repeatedly sends a flat nominal reading while the joint is actually overheating.
- Zero or negative torque reported while the arm is running under load.

**What it wouldn't catch:**
- Coordinated multi-sensor attacks where the attacker fakes all three sensors at once (torque, temperature, and vibration) to match a healthy profile.
- Very small, subtle value drifts that stay within normal operating ranges.
