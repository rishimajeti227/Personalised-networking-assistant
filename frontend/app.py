import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Networking Assistant", layout="centered")
st.title("🤝 Personalized Networking Assistant")

# ── Generate Conversation Starters ────────────────────────────────────────────

event_desc = st.text_area("Event Description", placeholder="Type the event details here...")
user_interests = st.text_input("Your Interests", placeholder="AI, Blockchain, Cyber Security")

if st.button("Generate Conversation Starters"):
    if event_desc and user_interests:
        parsed_interests = [i.strip() for i in user_interests.split(",") if i.strip()]
        payload = {"description": event_desc, "interests": parsed_interests}

        for key in ["topics", "suggestions", "topic_facts"]:
            st.session_state.pop(key, None)

        try:
            res = requests.post(f"{BASE_URL}/generate-conversation", json=payload)
            if res.status_code == 200:
                data = res.json()
                topics = data.get("topics", [])
                st.session_state["topics"] = topics
                st.session_state["suggestions"] = data.get("suggestions", [])

                # auto-fact-check each extracted topic so the user knows what they mean
                topic_facts = {}
                for topic in topics:
                    try:
                        fc_res = requests.post(f"{BASE_URL}/fact-check", json={"query": topic})
                        if fc_res.status_code == 200:
                            topic_facts[topic] = fc_res.json().get("summary", "")
                    except Exception:
                        pass
                st.session_state["topic_facts"] = topic_facts
            else:
                st.error("Backend encountered an operational exception.")
        except Exception:
            st.error("Could not establish a connection to the FastAPI gateway.")
    else:
        st.warning("Please fill in both the event description and your interests.")

if "suggestions" in st.session_state:
    st.subheader("🧠 Extracted Topics:")
    for idx, topic in enumerate(st.session_state["topics"]):
        st.write(f"{idx} : \"{topic}\"")

    topic_facts = st.session_state.get("topic_facts", {})
    if topic_facts:
        with st.expander("📚 What do these topics mean? (auto fact-checked)"):
            for topic, summary in topic_facts.items():
                st.markdown(f"**{topic}:** {summary}")

    st.subheader("💬 Conversation Starters:")
    if not st.session_state["suggestions"]:
        st.warning("No conversation starters could be generated.")

    for i, item in enumerate(st.session_state["suggestions"]):
        st.info(item)
        col1, col2 = st.columns([1, 1])

        if col1.button("👍 Like", key=f"like_{i}"):
            try:
                requests.post(f"{BASE_URL}/feedback", json={"suggestion": item, "action": "like"})
                st.toast("Feedback registered!")
            except Exception:
                st.error("Could not send feedback to the backend.")

        if col2.button("👎 Dislike", key=f"dislike_{i}"):
            try:
                requests.post(f"{BASE_URL}/feedback", json={"suggestion": item, "action": "dislike"})
                st.toast("Feedback registered!")
            except Exception:
                st.error("Could not send feedback to the backend.")

# ── Manual Fact Verification ──────────────────────────────────────────────────

st.markdown("---")
st.subheader("🛡️ Fact Verification")
st.caption("Verify topics before you speak.")

fact_query = st.text_input(
    "Enter a topic to verify",
    placeholder="e.g. GPT-2, blockchain, reinforcement learning",
    key="fact_query_input",
)

if st.button("Verify Fact", key="verify_fact_btn"):
    if fact_query.strip():
        try:
            fc_res = requests.post(f"{BASE_URL}/fact-check", json={"query": fact_query.strip()})
            if fc_res.status_code == 200:
                st.success(fc_res.json().get("summary", "No information found."))
            else:
                st.warning("Could not retrieve information for that topic.")
        except Exception:
            st.error("Could not connect to the fact-check service.")
    else:
        st.warning("Please enter a topic to verify.")

# ── Recent Sessions History ───────────────────────────────────────────────────

st.markdown("---")
st.subheader("📜 Recent Sessions History")

try:
    hist_resp = requests.get(f"{BASE_URL}/history")
    history_entries = hist_resp.json().get("history", []) if hist_resp.status_code == 200 else []
except Exception:
    history_entries = []
    st.warning("Could not load history from the backend.")

for h in reversed(history_entries):
    description_preview = (h.get("description") or "")[:60]
    st.text(f"Event: {description_preview}...")
    st.caption(
        f"Themes: {', '.join(h.get('topics', []))} | Timestamp: {h.get('timestamp')}"
    )
    st.markdown("---")

# ── Performance Telemetry Logs ────────────────────────────────────────────────

st.subheader("📊 Performance Telemetry Logs")

try:
    fb_resp = requests.get(f"{BASE_URL}/feedback-log")
    feedback_entries = fb_resp.json().get("feedback", []) if fb_resp.status_code == 200 else []
except Exception:
    feedback_entries = []

for f_entry in reversed(feedback_entries[-10:]):
    icon = "👍" if f_entry.get("feedback") == "like" else "👎"
    st.markdown(f"**{icon}** {f_entry.get('suggestion')}")
    st.caption(f"Logged at: {f_entry.get('timestamp')}")
