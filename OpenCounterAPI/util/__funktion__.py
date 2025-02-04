from datetime import datetime, timezone, timedelta
import json
import os

def load_data(page, DATA_DIR):
    file_path = os.path.join(DATA_DIR, f"{page}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {"user_count_sum": 0, "user_uniq": 0, "users": {}, "date_stats": {}}

def save_data(page, data, DATA_DIR):
    file_path = os.path.join(DATA_DIR, f"{page}.json")
    print(f"Save data to: {file_path}")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def update_date_stats(date_stats, now, user_ip):
    now_dt = datetime.fromisoformat(now)
    time_intervals = {
        "now": timedelta(minutes=15),
        "today": timedelta(days=1),
        "week": timedelta(weeks=1),
        "month": timedelta(days=30)
    }

    for key, delta in time_intervals.items():
        if key not in date_stats:
            date_stats[key] = [1, now, {"uniq_users": [user_ip]}]
        else:
            last_time = datetime.fromisoformat(date_stats[key][1])
            if now_dt - last_time <= delta:
                if user_ip not in date_stats[key][2]["uniq_users"]:
                    date_stats[key][0] += 1
                    date_stats[key][2]["uniq_users"].append(user_ip)
            else:
                date_stats[key] = [1, now, {"uniq_users": [user_ip]}]

    return date_stats

def remove_keys(data, keys_to_remove):

    """ Entfernt alle angegebenen Schlüssel rekursiv aus verschachtelten Strukturen. """
    if isinstance(data, dict):
        return {k: remove_keys(v, keys_to_remove) for k, v in data.items() if k not in keys_to_remove}
    elif isinstance(data, list):
        return [remove_keys(item, keys_to_remove) for item in data]
    else:
        return data

