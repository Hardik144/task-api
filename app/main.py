from fastapi import FastAPI

from app.routes import router
from app.database import initialize_database

app = FastAPI(
    title="Task API",
    description="FlyRank Backend Assignment",
    version="1.0.0"
)

initialize_database()

app.include_router(router)