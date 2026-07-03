import requests
from urllib.parse import quote
from app.config import FACT_CHECK_API

# Wikipedia requires a descriptive User-Agent — anonymous requests are often rate-limited
_HEADERS = {
    "User-Agent": "NetworkingAssistant/1.0 (educational-project; contact@example.com)"
}

# pre-seeded for the 10 standard themes so no network call is needed for common queries;
# also grows at runtime as new topics are successfully fetched
_cache: dict[str, str] = {
    "ai": "Artificial intelligence (AI) is intelligence demonstrated by machines, enabling them to perform tasks that typically require human intelligence such as learning, reasoning, and problem-solving.",
    "healthcare": "Healthcare is the maintenance or improvement of health via the prevention, diagnosis, treatment, and cure of disease, illness, and injury in people.",
    "blockchain": "A blockchain is a distributed ledger with growing lists of records (blocks) securely linked using cryptography — the foundation of cryptocurrencies like Bitcoin.",
    "education": "Education is the structured transmission of knowledge, values, and skills across generations, typically delivered via schools, universities, and digital platforms.",
    "sustainability": "Sustainability is the ability to meet present needs without compromising the ability of future generations to meet their own, especially regarding the environment.",
    "robotics": "Robotics is an interdisciplinary field combining computer science and engineering to design, build, and operate robots for automation, manufacturing, and exploration.",
    "cybersecurity": "Cybersecurity is the practice of protecting computer systems, networks, and data from digital attacks, unauthorised access, and damage.",
    "finance": "Finance is the study and management of money, investments, and other financial instruments across individuals, businesses, and governments.",
    "business": "Business is the activity of producing, buying, or selling goods and services in exchange for money, with the goal of generating profit.",
    "technology": "Technology is the application of scientific knowledge for practical purposes — especially in industry — including tools, machines, software, and systems.",
}


def fact_check(query: str) -> str:
    # normalise to lowercase for consistent cache key lookup
    q_lower = query.strip().lower()

    if q_lower in _cache:
        return _cache[q_lower]

    # Wikipedia titles use underscores; quote() handles any remaining special characters
    sanitized = query.strip().replace(" ", "_")
    encoded = quote(sanitized, safe="/_")

    try:
        response = requests.get(
            f"{FACT_CHECK_API}/{encoded}",
            headers=_HEADERS,
            timeout=2,
        )
        if response.status_code == 200:
            data = response.json()
            result = data.get("extract") or "No summary found."
        else:
            result = "Fact checking lookup yielded no match."
    except Exception:
        result = "Fact-checking interface encountered a network error."

    # only cache successful lookups, not error strings
    if not result.startswith("Fact-checking interface"):
        _cache[q_lower] = result

    return result
