import base64
import json
from datetime import datetime
from typing import Optional

from bson import json_util
from fastapi import APIRouter, Security, HTTPException, Response, Request
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from starlette.responses import RedirectResponse
import nanoid

from app import config

router = APIRouter()
security = HTTPBearer()


class NanoIdInputType(BaseModel):
    alphabets: Optional[str] = 'A-Za-z0-9_-'
    length: Optional[int] = 10

    class Config:
        schema_extra = {
            "example": {
                "alphabets": "1234567890abcdef",
                "length": 20
            }
        }


@router.get('/')
async def get_root():
    return await gen_nanoid_by_get(5)


@router.get('/{count}')
async def gen_nanoid_by_get(count: int = 5):
    """
    Generate x number of nano-id
    """
    result = [nanoid.generate() for i in range(count)]
    return {'result': result}


@router.post('/{count}')
async def shorten_url(payload: NanoIdInputType, count: int):
    """
    Generate x number of nano-id with specified alphabets and length
    """
    result = [nanoid.generate(payload.alphabets, payload.length) for i in range(count)]
    return {'result': result, 'alphabets': payload.alphabets, 'length': payload.length}
