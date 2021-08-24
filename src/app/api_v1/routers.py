from fastapi import APIRouter

from app.api_v1 import user_auth

routers = APIRouter()
routers.include_router(
    user_auth.router, prefix="/auth", tags=["Auth"])
