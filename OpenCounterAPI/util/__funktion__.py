from datetime import datetime, timezone, timedelta
import calendar
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


def get_next_midnight(now_dt):
    """Returns the date with 23:59:59 for today."""
    return now_dt.replace(hour=23, minute=59, second=59, microsecond=0)

def get_next_sunday_midnight(now_dt):
    """Returns the date of the next Sunday at 23:59:59."""
    days_until_sunday = (6 - now_dt.weekday()) % 7  # 0 (Monday) to 6 (Sunday)
    next_sunday = now_dt + timedelta(days=days_until_sunday)
    return next_sunday.replace(hour=23, minute=59, second=59, microsecond=0)

def get_last_day_of_month_midnight(now_dt):
    """Returns the last day of the month at 23:59:59."""
    last_day = calendar.monthrange(now_dt.year, now_dt.month)[1]  # Last day of the month
    last_day_dt = now_dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=0)
    return last_day_dt

def update_date_stats(date_stats, now, user_ip):
    """
    Updates the expiration time for different intervals (now, today, week, month)
    and tracks unique users accessing within these intervals.
    """
    now_dt = datetime.fromisoformat(now)

    # Convert now_dt to UTC-aware datetime (assuming it's in UTC)
    if now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=timezone.utc)

    current_time = datetime.now(timezone.utc)  # Ensure timezone-aware comparison

    # Ensure now_dt is not in the past
    if now_dt < current_time:
        now_dt = current_time

    # Define expiration times for different intervals
    new_expire_times = {
        "now": now_dt + timedelta(minutes=15),
        "today": get_next_midnight(now_dt),
        "week": get_next_sunday_midnight(now_dt),
        "month": get_last_day_of_month_midnight(now_dt)
    }

    for key, new_expire_time in new_expire_times.items():
        if key in date_stats:
            last_expire_time = datetime.fromisoformat(date_stats[key][1])

            # Convert to timezone-aware datetime
            if last_expire_time.tzinfo is None:
                last_expire_time = last_expire_time.replace(tzinfo=timezone.utc)

            # If the interval has expired, reset it
            if now_dt > last_expire_time:
                date_stats[key] = [1, new_expire_time.isoformat(), {"uniq_users": [user_ip]}]
            else:  # If the interval is still valid
                if user_ip not in date_stats[key][2]["uniq_users"]:
                    date_stats[key][0] += 1
                    date_stats[key][2]["uniq_users"].append(user_ip)
        else:  # If the interval does not exist yet
            date_stats[key] = [1, new_expire_time.isoformat(), {"uniq_users": [user_ip]}]

    return date_stats


def remove_keys(data, keys_to_remove):

    """ Entfernt alle angegebenen Schlüssel rekursiv aus verschachtelten Strukturen. """
    if isinstance(data, dict):
        return {k: remove_keys(v, keys_to_remove) for k, v in data.items() if k not in keys_to_remove}
    elif isinstance(data, list):
        return [remove_keys(item, keys_to_remove) for item in data]
    else:
        return data

