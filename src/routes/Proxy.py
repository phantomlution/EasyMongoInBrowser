# -*- coding:utf-8 -*-
import requests
import json
from flask import Blueprint, request, Response
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


proxy_api = Blueprint('proxy_api', __name__, url_prefix='/proxy')

session = requests.session()


# 定义重试策略
retry_strategy = Retry(
    total=3,  # 最大重试次数（包括第一次请求）
    status_forcelist=[500, 502, 503, 504]  # 遇到这些状态码时重试（可选）
)

# 将重试策略应用到 Session 的 HTTP 和 HTTPS 适配器
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)


@proxy_api.route('/get', methods=['POST'])
def get_data():
    params = request.get_json()

    url = params.get('url')

    headers = params.get('headers')

    query = params.get('query')

    data = params.get('data')

    json = params.get('json')

    cookies = params.get('cookies', {})

    charset = params.get('charset')

    timeout = params.get('timeout', 3)

    proxies = params.get('proxy')

    request_method = params.get('method', 'get')

    request_func = getattr(session, request_method.lower())

    resp = request_func(url, headers=headers, proxies=proxies, params=query, data=data, json=json, cookies=cookies, timeout=timeout)

    resp.close()

    raw_content = resp.content

    if charset:
        try:
            raw_content = raw_content.decode(charset).encode('utf-8')
        except:
            pass

    response = Response(raw_content)

    cookie_arr = []

    for item in resp.cookies:
        cookie_arr.append(item.name + '=' + item.value)

    response.headers['Access-Control-Expose-Headers'] = 'x-cookie'

    if len(cookie_arr) > 0:
        response.headers['x-cookie'] = '; '.join(cookie_arr)

    return response


@proxy_api.route('/form', methods=['POST'])
def post_form():
    url = request.args.get('url')

    headers = json.loads(request.args.get('headers'))

    if 'file' in request.files:
        file = request.files['file']
        files = {'file': (file.filename, file.stream, file.mimetype)}
    else:
        files = None

    data = request.form.to_dict()

    resp = requests.post(url=url, files=files, data=data, headers=headers)

    resp.close()

    raw_content = resp.content

    response = Response(raw_content)

    return response




@proxy_api.route('/image', methods=['GET'])
def get_image():
    url = request.args.get('url')

    resp = session.get(url)

    resp.close()

    return resp.content
