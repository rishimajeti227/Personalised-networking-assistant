from transformers import pipeline
from app.config import MODEL_NAMES

# loaded once at module level — DistilBERT is ~250 MB and slow to initialise per request
classifier = pipeline("zero-shot-classification", model=MODEL_NAMES["event_analysis"])

# broad default set; callers can pass custom labels to narrow the scope
_DEFAULT_LABELS = [
    "AI", "healthcare", "blockchain", "education", "sustainability",
    "robotics", "cybersecurity", "finance", "business", "technology",
]


def extract_event_themes(description: str, candidate_labels=None) -> list:
    # returns the top 3 highest-scoring labels for the given description
    if candidate_labels is None:
        candidate_labels = _DEFAULT_LABELS
    result = classifier(description, candidate_labels)
    return result["labels"][:3]
