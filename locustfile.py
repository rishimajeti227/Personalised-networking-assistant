# locustfile.py
from locust import HttpUser, task, between


class NetworkingAssistantUser(HttpUser):
    # Delay between tasks to simulate user behaviour
    wait_time = between(1, 3)

    @task(2)
    def generate_conversation(self):
        """Hit the conversation starter generation pipeline."""
        payload = {
            "description": "AI in public health summit discussing data ethics",
            "interests": ["AI", "healthcare", "machine learning"],
        }
        self.client.post("/generate-conversation", json=payload)

    @task(1)
    def fact_check(self):
        """Hit the Wikipedia fact-checking endpoint."""
        payload = {
            "query": "healthcare",
        }
        self.client.post("/fact-check", json=payload)
