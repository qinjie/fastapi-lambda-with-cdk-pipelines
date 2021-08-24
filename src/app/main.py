from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.api_v1.routers import routers as v1_api_router
from app.config import API_GATEWAY_STAGE

# Set openapi_prefix to stag value, e.g. dev, so that /docs works
prefix = f'/{API_GATEWAY_STAGE}' if API_GATEWAY_STAGE else ''
print(prefix)
app = FastAPI(openapi_prefix=prefix)

# Enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def get_root(response: Response):
    return {'message': 'Welcome to User Auth API'}


app.include_router(v1_api_router, prefix="/v1")

# Wrap API with Mangum
handler = Mangum(app)
