from pymongo import MongoClient
from bson import ObjectId

mongo_instance = MongoClient('mongodb://localhost:27017')


# 更新 _id
def format_query(query):
    if '_id' in query:
        query['_id'] = ObjectId(query['_id'])


class MongoService:

    @staticmethod
    def get(db, table_name, query):
        format_query(query)
        return mongo_instance[db][table_name].find_one(query)

    @staticmethod
    def save(db, table_name, data):
        return mongo_instance[db][table_name].insert(data)

    @staticmethod
    def update(db, table_name, query, data):
        format_query(query)
        return mongo_instance[db][table_name].find_one_and_update(query, { "$set": data })

    @staticmethod
    def list(db, table_name, query):
        format_query(query)
        return list(mongo_instance[db][table_name].find(query))

    @staticmethod
    def remove(db, table_name, query):
        format_query(query)
        return mongo_instance[db][table_name].find_one_and_delete(query)