from app.services.event_analyzer import extract_event_themes


def test_extract_themes_returns_list():
    themes = extract_event_themes("Tech conference on Artificial Intelligence and Neural Networks")
    assert isinstance(themes, list)
    assert len(themes) <= 3


def test_extract_themes_at_least_one_result():
    themes = extract_event_themes("Annual healthcare innovation summit")
    assert len(themes) >= 1


def test_extract_themes_filtering():
    # all returned themes must come from the provided candidate set
    candidates = ["AI", "healthcare", "blockchain"]
    themes = extract_event_themes("Medical diagnostics app demo", candidate_labels=candidates)
    for t in themes:
        assert t in candidates


def test_extract_themes_with_custom_labels():
    candidates = ["education", "sustainability", "finance"]
    themes = extract_event_themes("Green energy investment forum", candidate_labels=candidates)
    assert isinstance(themes, list)
    for t in themes:
        assert t in candidates
