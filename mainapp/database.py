from pymongo.mongo_client import MongoClient
from django.conf import settings
db_connection = None

def get_database_connection():
    global db_connection

    if db_connection is None:
        # Create a new database connection
        client = MongoClient(settings.MONGO_DB['host'])
        db = client[settings.MONGO_DB['name']]
        db_connection = client["Mydb"]
    
    return db_connection