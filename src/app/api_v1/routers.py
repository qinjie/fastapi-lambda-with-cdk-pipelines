from fastapi import APIRouter
from app import config
from app.api_v1 import nanoid_api

routers = APIRouter()
routers.include_router(nanoid_api.router, prefix="/nanoid")
