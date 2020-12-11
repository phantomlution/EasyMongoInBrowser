# -*- coding:utf-8 -*-
import requests
from flask import Blueprint, request, Response

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

    resp = request_func(url=url, headers=headers, params=query, data=data, verify=False)

    resp.close()

    response = Response(resp.content)

    response.headers['Access-Control-Expose-Headers'] = 'x-cookie'
    if 'set-cookie' in resp.headers:
        response.headers['x-cookie'] = resp.headers['set-cookie']

    return response


@proxy_api.route('/image', methods=['GET'])
def get_image():
    url = request.args.get('url')

    resp = session.get(url)

    resp.close()

    return resp.content