from fastapi import FastAPI
from app.routers import conversation

app = FastAPI(
    title="Personalized Networking Assistant",
    description="AI-powered backend for extracting event themes and generating conversation starters.",
    version="1.0.0",
)

app.include_router(conversation.router)


# health-check endpoint — confirms the server is up
@app.get("/")
def root():
    return {"message": "Welcome to the Networking Assistant API!"}
