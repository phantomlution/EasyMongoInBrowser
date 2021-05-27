# -*- coding:utf-8 -*-
import requests
from flask import Blueprint, request, Response

proxy_api = Blueprint('proxy_api', __name__, url_prefix='/proxy')

session = requests.Session()


@proxy_api.route('/get', methods=['POST'])
def get_data():
    params = request.get_json()

    url = params.get('url')

    headers = params.get('headers')

    query = params.get('query')

    data = params.get('data')

    cookies = params.get('cookies', {})

    charset = params.get('charset')

    request_method = params.get('method', 'get')

    request_func = getattr(session, request_method.lower())

    resp = request_func(url, headers=headers, params=query, data=data, verify=False, cookies=cookies)

    resp.close()

    raw_content = resp.content

    if charset:
        raw_content = raw_content.decode(charset).encode('utf-8')

    response = Response(raw_content)

    cookie_arr = []

    for item in resp.cookies:
        cookie_arr.append(item.name + '=' + item.value)

    response.headers['Access-Control-Expose-Headers'] = 'x-cookie'

    if len(cookie_arr) > 0:
        response.headers['x-cookie'] = '; '.join(cookie_arr)

    return response


@proxy_api.route('/image', methods=['GET'])
def get_image():
    url = request.args.get('url')

    resp = session.get(url)

    resp.close()

    return resp.content