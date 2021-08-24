import datetime
from uuid import uuid4

import jwt
from fastapi import HTTPException

JWT_SECRET = b'\xf7\xb6k\xabP\xce\xc1\xaf\xad\x86\xcf\x84\x02\x80\xa0\xe0'


def gen_jwt_token(payload_data, jwt_secret=JWT_SECRET, valid_hours=24):
    now = datetime.datetime.utcnow()
    unique_id = str(uuid4())
    payload = {
        'sub': payload_data,
        'iat': now,
        'jti': unique_id,
    }
    if valid_hours and valid_hours > 0:
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=valid_hours)

    return jwt.encode(payload, jwt_secret, algorithm='HS256')


def decode_jwt_token(jwt_token, jwt_secret=JWT_SECRET):
    try:
        return jwt.decode(jwt_token, jwt_secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("Exception: Token expired. Get new one")
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        print("Exception: Invalid Token")
        raise HTTPException(status_code=401, detail='Invalid token')


if __name__ == '__main__':
    token = gen_jwt_token({'message': 'Hello World'}, JWT_SECRET)
    print(token)
    data = decode_jwt_token(token, JWT_SECRET)
    print(data)
