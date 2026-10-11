import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = "System-Automation-Psg-23i213\day2\data\day2_sample.csv"

def train_model():
    df = pd.read_csv(DATA_PATH)
    x = df[["temperature", "pressure", "vibration", "rpm", "current"]]
    y = df["state"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42
    )

    model = DecisionTreeClassifier(max_depth=4,random_state=42)
    model.fit(x_train, y_train)
    print("Hold-out Accuracy:", model.score(x_test, y_test))
    
    return model

if __name__ == "__main__":
    model = train_model()