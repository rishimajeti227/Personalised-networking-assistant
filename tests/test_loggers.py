import pytest
from unittest.mock import patch
from app.services import history_logger, feedback_logger


def test_history_logger_lifecycle(tmp_path):
    history_logger.HISTORY_FILE = tmp_path / "history.json"
    assert history_logger.load_history() == []

    history_logger.log_conversation({"description": "Test Event"})

    populated = history_logger.load_history()
    assert len(populated) == 1
    assert populated[0]["description"] == "Test Event"


def test_history_logger_write_corrupt(tmp_path):
    # verifies that logging to a corrupt file recovers and writes cleanly
    history_logger.HISTORY_FILE = tmp_path / "corrupt_write_hist.json"
    with open(history_logger.HISTORY_FILE, "w") as f:
        f.write("{invalid json...")

    history_logger.log_conversation({"description": "Recovered Event"})
    assert len(history_logger.load_history()) == 1


def test_history_logger_read_exception():
    # patches Path.read_text (not builtins.open) because storage.py uses read_text()
    with patch("pathlib.Path.read_text", return_value="{bad_json"):
        with patch("pathlib.Path.exists", return_value=True):
            assert history_logger.load_history() == []


def test_feedback_logger_lifecycle(tmp_path):
    feedback_logger.FEEDBACK_FILE = tmp_path / "feedback.json"
    assert feedback_logger.get_feedback() == []

    feedback_logger.log_feedback("Icebreaker 1", "like")

    populated = feedback_logger.get_feedback()
    assert len(populated) == 1
    assert populated[0]["suggestion"] == "Icebreaker 1"


def test_feedback_logger_write_corrupt(tmp_path):
    # verifies that logging to a corrupt file recovers and writes cleanly
    feedback_logger.FEEDBACK_FILE = tmp_path / "corrupt_write_feed.json"
    with open(feedback_logger.FEEDBACK_FILE, "w") as f:
        f.write("bad payload structure")

    feedback_logger.log_feedback("Recovered context", "dislike")
    assert len(feedback_logger.get_feedback()) == 1


def test_feedback_logger_read_exception():
    with patch("pathlib.Path.read_text", return_value="!!!invalid text!!!"):
        with patch("pathlib.Path.exists", return_value=True):
            assert feedback_logger.get_feedback() == []