# -*- coding:utf-8 -*-
import requests
from flask import Blueprint, request

proxy_api = Blueprint('proxy_api', __name__, url_prefix='/proxy')

session = requests.Session()


@proxy_api.route('/get', methods=['POST'])
def get_data():
    params = request.get_json()

    url = params['url']

    headers = params.get('headers')

    query = params.get('query')

    data = params.get('data')

    request_method = params.get('method', 'get')

    request_func = getattr(session, request_method.lower())

    resp = request_func(url=url, headers=headers, params=query, data=data)

    resp.close()

    return resp.content

