from pymongo import MongoClient, ASCENDING

from app.config import DB, USER, PWD, SERVER, COLL_USERS, COLL_OTP, COLL_JWT


def create_index_for_collections(target_db):
    if COLL_USERS not in target_db.list_collection_names():
        target_db[COLL_USERS].create_index([('email', ASCENDING)], unique=True)
    if COLL_OTP not in target_db.list_collection_names():
        target_db[COLL_OTP].create_index([('email', ASCENDING), ('otp', ASCENDING)])
    if COLL_JWT not in target_db.list_collection_names():
        target_db[COLL_JWT].create_index([('jwt', ASCENDING)], unique=True)


mongodb_url = f'mongodb+srv://{USER}:{PWD}@{SERVER}/{DB}?retryWrites=true&w=majority'
db = None

try:
    client = MongoClient(mongodb_url)
    if DB not in client.list_database_names():
        print('Create database')
        create_index_for_collections(client[DB])

    db = client[DB]
    print('Connected to MongoDB')
except Exception as e:
    print(repr(e))
    raise Exception(f'Error in MongoDB connection. {mongodb_url}')
