import json
import os
from datetime import datetime

# ✅ Updated path for deployment
FILE_PATH = "app/data/attendance.json"


def load_data():
    # ✅ Ensure file exists
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_data(data):
    # ✅ Ensure folder exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def mark_attendance(user_name):
    data = load_data()
    today = str(datetime.now().date())

    # ✅ Check duplicate
    for record in data:
        if record["name"] == user_name and record["date"] == today:
            return "Already marked"

    # ✅ Add new record
    new_record = {
        "name": user_name,
        "date": today,
        "time": str(datetime.now())
    }

    data.append(new_record)
    save_data(data)

    return "Attendance marked"