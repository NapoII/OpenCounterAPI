"""Full Doku on: https://github.com/NapoII/open_page_counter_api"
-----------------------------------------------
!!! ADD MUST HAVE INFO !!
------------------------------------------------
"""
api_version = "1.0.1"
#### import

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from util.__funktion__ import *
from util.__my_path_funktion__ import *

my_file_path = my_file_path()

#### Main
print(f"OpenCounterAPI - starts running")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
DATA_DIR = my_file_path.json.data_dir

print(f'DATA_DIR: {DATA_DIR}')
if not os.path.exists(DATA_DIR):
    print(f'Create data dir: {DATA_DIR}')
    os.makedirs(DATA_DIR)

@app.route("/api/counter", methods=["POST"])
def counter():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(',')[0].strip()

    page_name = data.get("page_name", "no_page_name")

    now = datetime.now(timezone.utc).isoformat()

    additional_data = {
        "browser": data.get("browser", "unknown"),
        "screen_width": data.get("screen_width", "unknown"),
        "screen_height": data.get("screen_height", "unknown"),
        "viewport_width": data.get("viewport_width", "unknown"),
        "viewport_height": data.get("viewport_height", "unknown"),
        "referrer": data.get("referrer", "unknown"),
        "language": data.get("language", "unknown"),
        "os": data.get("os", "unknown"),
        "timestamp": data.get("timestamp", now),
        "page_name": data.get("page_name", "no_page_name")
    }

    page_data = load_data(page_name, DATA_DIR)  # Lade die Daten aus der festen Datei

    if "date_stats" not in page_data:
        page_data["date_stats"] = {}

    page_data["date_stats"] = update_date_stats(page_data["date_stats"], now, user_ip)

    if user_ip not in page_data["users"]:
        page_data["users"][user_ip] = {
            "count": 0,
            "last_seen": now,
            "timestamps": [],
            "details": additional_data
        }
        page_data["user_uniq"] += 1

    user_data = page_data["users"][user_ip]

    user_data["count"] += 1
    user_data["last_seen"] = now
    user_data["timestamps"].append(now)
    user_data["details"] = additional_data
    page_data["user_count_sum"] += 1

    save_data(page_name, page_data, DATA_DIR)  # Speichere die Daten in der festen Datei

    # Schlüssel, die entfernt werden sollen
    keys_to_remove = {"uniq_users", "users"}
    cleaned_data = remove_keys(page_data, keys_to_remove)

    response_data = {
        "user_count_sum": cleaned_data["user_count_sum"],
        "user_uniq": cleaned_data["user_uniq"],
        "count": user_data["count"],
        "date_stats": cleaned_data["date_stats"],
        "api_version": api_version
    }

    return jsonify(response_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8800)
