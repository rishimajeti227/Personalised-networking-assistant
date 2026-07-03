# central place to change model names and external API URLs without touching service code
MODEL_NAMES = {
    "event_analysis": "typeform/distilbert-base-uncased-mnli",  # zero-shot classifier
    "text_generator": "gpt2",                                    # completion model for starters
}

FACT_CHECK_API = "https://en.wikipedia.org/api/rest_v1/page/summary"
