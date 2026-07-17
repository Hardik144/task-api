from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    description="FlyRank Backend Assignment",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Task API!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }