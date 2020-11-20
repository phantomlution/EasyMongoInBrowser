import requests
from flask import Blueprint, request

proxy_api = Blueprint('proxy_api', __name__, url_prefix='/proxy')


@proxy_api.route('/get', methods=['POST'])
def get_data():
    params = request.get_json()

    url = params['url']

    headers = params.get('headers')

    query = params.get('query')

    data = params.get('data')

    request_method = params.get('method', 'get')

    request_func = getattr(requests, request_method)

    resp = request_func(url=url, headers=headers, params=query, data=data)

    return resp.content

