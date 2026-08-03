from fastapi import FastAPI

app = FastAPI(
    title="Foothold",
    description="AI-powered job search assistant",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Foothold is running!"
    }