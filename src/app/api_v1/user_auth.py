import json
from random import randint

from bson import json_util
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic import EmailStr

from app.config import COLL_USERS, COLL_OTP, COLL_JWT, COLL_APPS
from app.database import db
from app.utils.auth_util import JWT_SECRET, gen_jwt_token, decode_jwt_token
from app.utils.emailer_sender import email_otp
from app.utils.json_encoder import JSONEncoder

router = APIRouter()


class EmailType(BaseModel):
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "email": 'mark.qj@gmail.com'
            }
        }


class EmailOtpType(BaseModel):
    email: EmailStr
    otp: int

    class Config:
        schema_extra = {
            "example": {
                "email": "mark.qj@gmail.com",
                "otp": "12345"
            }
        }


def gen_otp():
    i = randint(1, 10 ** 5)
    return pad_int(i)


def pad_int(i):
    return f'{i:05}'


@router.post('/get_otp_email', response_class=ORJSONResponse)
async def get_otp_email(payload: EmailType, response: Response):
    """
    Request for an OTP to be sent to a registered email.
    """
    email = payload.email
    print(email)
    coll_users = COLL_USERS
    coll_otp = COLL_OTP

    # Find record matches either emails or emp_nums
    user = db[coll_users].find_one({'email': email})
    if user is None:
        raise HTTPException(status_code=401, detail="You are not a registered user")

    # Generate and save OTP
    otp = gen_otp()
    result = db[coll_otp].insert_one({'email': email, 'otp': otp})
    print(result)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Error in inserting OTP to database")

    # Email OTP
    name = user['name']
    email_otp(otp, [email], name=name)

    return {'message': 'An OTP has been emailed to you.'}


@router.post('/get_jwt_token', response_class=ORJSONResponse)
async def get_jwt_token(payload: EmailOtpType, response: Response):
    """
    Request for a JWT token
    """
    email = payload.email
    otp = pad_int(payload.otp)

    coll_users = COLL_USERS
    coll_otp = COLL_OTP
    coll_jwt = COLL_JWT
    coll_apps = COLL_APPS

    # Find record matches either emails or emp_nums
    user = db[coll_users].find_one({'email': email})
    if user is None:
        raise HTTPException(status_code=401, detail="You are not a registered user")
    print(json_util.dumps(user))

    # Generate and save OTP
    record = db[coll_otp].find_one({'email': email, 'otp': otp})
    if record is None:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    print(json_util.dumps(record))

    # Generate JWT which contains user's permissions
    jwt_token = gen_jwt_token(json_util.dumps(user), JWT_SECRET)
    print(jwt_token)
    # temp = decode_jwt_token(jwt_token, JWT_SECRET)
    # print(temp)

    # Update/Insert JWT into database
    result = db[coll_jwt].update({'email': email}, {"$set": {"jwt": jwt_token}}, upsert=True)
    print(json_util.dumps(result))

    # Get apps permission of this user
    permissions = db[coll_apps].find({"name": {"$in": user['permissions']}})
    apps = []
    for p in permissions:
        p.pop('_id')
        apps.append(p)

    return {'jwt': jwt_token, 'apps': apps}


@router.get('/get_apps', response_class=ORJSONResponse)
async def get_apps(response: Response):
    """
    Return list of available app modules
    """
    coll_apps = COLL_APPS

    # Find record matches either emails or emp_nums
    with db[coll_apps].find({}) as cursor:
        records = list(cursor)
        print(records)
    result = json.loads(json_util.dumps(records))
    return {"apps": result}
