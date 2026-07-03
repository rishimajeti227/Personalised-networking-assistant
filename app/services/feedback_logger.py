from datetime import datetime
from pathlib import Path
from app.services.storage import load_json, save_json

FEEDBACK_FILE = Path("feedback.json")


def log_feedback(suggestion: str, action: str) -> None:
    # stamps every entry with an ISO timestamp before appending
    entry = {
        "suggestion": suggestion,
        "feedback": action,
        "timestamp": datetime.now().isoformat(),
    }
    data = get_feedback()
    data.append(entry)
    save_json(FEEDBACK_FILE, data)


def get_feedback() -> list:
    return load_json(FEEDBACK_FILE, default=[])
