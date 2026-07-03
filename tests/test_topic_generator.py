from app.services.topic_generator import generate_topics


def test_generate_topics_format():
    suggestions = generate_topics(["AI", "networking"], ["Coding"])
    assert isinstance(suggestions, list)
    assert len(suggestions) == 3
    for suggestion in suggestions:
        assert isinstance(suggestion, str)
        assert len(suggestion.strip()) > 0


def test_generate_topics_returns_three_starters():
    suggestions = generate_topics(["AI", "robotics"], ["cybersecurity", "robotics"])
    assert len(suggestions) == 3
    assert all(isinstance(s, str) and len(s) > 10 for s in suggestions)


def test_generate_topics_uses_theme_and_interest():
    suggestions = generate_topics(["blockchain", "finance"], ["finance", "blockchain"])
    assert len(suggestions) == 3
    # at least one starter should mention a theme or interest from the inputs
    combined = " ".join(suggestions).lower()
    assert "blockchain" in combined or "finance" in combined