import config
from random import randint
import uuid
from pymongo import MongoClient


try:
    mongo_client = MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    collection = mongo_client[config.MONGO_DB_NAME][config.MONGO_DB_COL_NAME]
except Exception as e:
    raise("MongoDB can't connected")


for i in range(1000):
    priority = randint(1, 1000)
    url = uuid.uuid4().hex
    fake = {
        "interval" : randint(10, 60),
        "priority" : priority,
        "data" : {
            "url" : url,
            "priority" : priority,
            "others" : "something more..."
        }
    }
    collection.insert_one(fake)
print('all done')