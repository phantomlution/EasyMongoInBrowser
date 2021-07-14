# -*- coding:utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_instance = MongoClient('mongodb://localhost:27017')


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
        
        result = mongo_instance[db][table_name].find_one_and_update(query, { "$set": data }, upsert=True)

        return result

    @staticmethod
    def list(db, table_name, query, projection, sort):
        format_query(query)

        if sort is None:
            return list(mongo_instance[db][table_name].find(query, projection))
        else:
            sort_rule_list = []
            for sort_rule in sort:
                sort_rule_list.append((sort_rule['k'], sort_rule['v']))
            return list(mongo_instance[db][table_name].find(query, projection).sort(sort_rule_list))

    @staticmethod
    def remove(db, table_name, query):
        format_query(query)
        return mongo_instance[db][table_name].remove(query)

    @staticmethod
    def page(db, table_name, query, page_number, page_size):
        format_query(query)

        return list(mongo_instance[db][table_name].find(query).skip(page_number * page_size).limit(page_size))