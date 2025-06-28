from fastapi import APIRouter
from api.v1.endpoints import webhook

api_router = APIRouter()
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
