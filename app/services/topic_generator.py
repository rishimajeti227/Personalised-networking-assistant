import re
from transformers import pipeline, set_seed
from app.config import MODEL_NAMES

# loaded once at module level — GPT-2 weights take ~500 MB and several seconds to load
generator = pipeline("text-generation", model=MODEL_NAMES["text_generator"])
# fixed seed so the same input always produces the same starters (reproducible demos)
set_seed(42)


def _clean_starter(generated_text: str, prompt: str) -> str:
    # GPT-2 returns the full prompt + completion; we only want the part after the opening quote
    quote_idx = prompt.rfind('"')
    if quote_idx != -1 and quote_idx < len(generated_text):
        text = generated_text[quote_idx + 1:]
    else:
        text = generated_text[len(prompt):]

    # trim at the closing quote or paragraph break, whichever comes first
    for end_char in ['"', "\n\n"]:
        idx = text.find(end_char)
        if idx != -1:
            text = text[:idx]

    # keep at most 2 sentences so starters don't run too long
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    text = " ".join(sentences[:2]).strip().strip("-").strip()

    # add an ellipsis if GPT-2 ran out of tokens before finishing a sentence
    if text and text[-1] not in ".!?\"":
        text += "..."

    return text


def _is_usable(text: str) -> bool:
    # rejects GPT-2 hallucinations: too short/long, or contains URLs / hashtags / stat patterns
    if len(text) < 15 or len(text) > 200:
        return False
    if re.search(r"https?://|www\.|#\w+|\d+x\b|[<>{}]", text, re.I):
        return False
    return True


def generate_topics(event_themes: list, user_interests: list) -> list:
    # join lists into strings for the prompt templates
    themes_str = ", ".join(event_themes) if event_themes else "technology"
    interests_str = ", ".join(user_interests) if user_interests else "networking"

    # each prompt leads GPT-2 into a different conversational angle;
    # the opening quote primes it to produce a natural spoken sentence
    prompts = [
        (
            f"At a {themes_str} networking event, a great opening line would be: "
            f'"As someone interested in {interests_str},'
        ),
        (
            f"A creative icebreaker for a {themes_str} conference: "
            f'"I\'ve been following the latest in {interests_str} and'
        ),
        (
            f"Starting a conversation at a {themes_str} meetup: "
            f'"What excites me most about'
        ),
    ]

    # per-slot fallbacks used when the model output fails the _is_usable check
    fallbacks = [
        f"As someone interested in {interests_str}, I'd love to hear how you're approaching {themes_str}.",
        f"I've been following the latest in {interests_str} — what's your take on where {themes_str} is heading?",
        f"What excites me most about {themes_str} is how fast it's moving — are you working in this space?",
    ]

    starters = []
    for prompt, fallback in zip(prompts, fallbacks):
        output = generator(
            prompt,
            max_new_tokens=40,
            num_return_sequences=1,
            do_sample=True,
            top_k=50,
            top_p=0.92,
            temperature=0.8,
            pad_token_id=generator.tokenizer.eos_token_id,
        )
        text = _clean_starter(output[0]["generated_text"], prompt)
        starters.append(text if _is_usable(text) else fallback)

    return starters[:3]
