from datetime import datetime
from pathlib import Path
from app.services.storage import load_json, save_json

HISTORY_FILE = Path("history.json")


def log_conversation(data: dict) -> None:
    # stamps every entry with an ISO timestamp before appending
    data["timestamp"] = datetime.now().isoformat()
    history = load_history()
    history.append(data)
    save_json(HISTORY_FILE, history)


def load_history() -> list:
    return load_json(HISTORY_FILE, default=[])
