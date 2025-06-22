
import json
import os
from datetime import datetime

LOG_PATH = "session_log.json"

def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def save_log(data):
    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

def insert_session(entry):
    log = load_log()
    log.append(entry)
    save_log(log)

def update_session(session_id, new_data):
    log = load_log()
    for entry in log:
        if entry.get("session_id") == session_id:
            entry.update(new_data)
            break
    else:
        print(f" session_id {session_id} not found, creating new.")
        new_entry = {"session_id": session_id}
        new_entry.update(new_data)
        log.append(new_entry)
    save_log(log)


