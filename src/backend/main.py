
from fastapi import FastAPI
from src.backend.api.routes.auth_routes import router as auth_router

app = FastAPI(
    title="Finsight AI API",
    description="Backend API for Finsight AI",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Finsight AI API is running"}
