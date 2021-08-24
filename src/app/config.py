import os

from dotenv import load_dotenv

load_dotenv()

API_MODULE_NAME = 'user_auth'

# MongoDB attributes
SERVER = os.getenv('MONGODB_SERVER')
USER = os.getenv('MONGODB_USER')
PWD = os.getenv('MONGODB_PWD')
DB = os.getenv('MONGODB_DB')
COLL_USERS = os.getenv('MONGODB_COLL_USERS', 'users')
COLL_OTP = os.getenv('MONGODB_COLL_OTP', 'otp')
COLL_JWT = os.getenv('MONGODB_COLL_JWT', 'jwt')
COLL_APPS = os.getenv('MONGODB_COLL_APPS', 'apps')

SES_REGION = os.environ.get('SES_REGION', 'ap-southeast-1')
SNS_REGION = os.environ.get('SNS_REGION', 'ap-southeast-1')
LAMBDA_REGION = os.environ.get('LAMBDA_REGION', 'ap-southeast-1')

EMAIL_ADMIN = os.environ.get('EMAIL_ADMIN', 'mark.qj@gmail.com')

# API Gateway
API_GATEWAY_STAGE = os.getenv('API_GATEWAY_STAGE', '')

print([SERVER, DB])
