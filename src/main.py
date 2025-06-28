from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="Webhook Explainer",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")

# To run the app: uvicorn main:app --reload
