# -*- coding:utf-8 -*-
from flask import Blueprint, request
from utils.decorator import flask_response
from service.MongoService import MongoService

mongo_api = Blueprint('mongo_api', __name__, url_prefix='/mongo')


@mongo_api.route('/get', methods=['POST'])
@flask_response
def get_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params['query']

    return MongoService.get(db, table_name, query)


@mongo_api.route('/save', methods=['POST'])
@flask_response
def save_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    data = params['data']

    return MongoService.save(db, table_name, data)


@mongo_api.route('/update', methods=['POST'])
@flask_response
def update_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params['query']
    data = params['data']

    return MongoService.update(db, table_name, query, data)


@mongo_api.route('/remove', methods=['POST'])
@flask_response
def delete_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params['query']

    return MongoService.remove(db, table_name, query)


@mongo_api.route('/query', methods=['POST'])
@flask_response
def query_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params.get('query', {})

    return MongoService.list(db, table_name, query)


@mongo_api.route('/list', methods=['POST'])
@flask_response
def list_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params.get('query', {})
    projection = params.get('projection', None)

    return MongoService.list(db, table_name, query, projection)


@mongo_api.route('/page', methods=['POST'])
@flask_response
def page_data():
    params = request.get_json()

    db = params['db']
    table_name = params['tableName']
    query = params.get('query', {})

    page_number = params.get('pageNumber', 1)
    page_size = params.get('pageSize', 20)

    return MongoService.page(db, table_name, query, page_number, page_size)