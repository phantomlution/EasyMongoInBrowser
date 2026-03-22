# -*- coding:utf-8 -*-
import requests
import json
from flask import Blueprint, request, Response


proxy_api = Blueprint('proxy_api', __name__, url_prefix='/proxy')

session = requests.session()


@proxy_api.route('/request', methods=['POST'])
def proxy():
    params = request.get_json()

    try:
        # 5. 转发请求
        resp = requests.request(
            method=params.get('method'),
            url=params.get('url'),
            headers=params.get('headers'),
            data=params.get('data'),
            # cookies=request.cookies,
            params=params.get('params'),
            allow_redirects=False
        )

        # return resp
        # # 6. 过滤掉不应转发回前端的响应头
        # excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        # resp_headers = [
        #     (name, value) for name, value in resp.raw.headers.items()
        #     if name.lower() not in excluded_headers
        # ]
        #
        # # 7. 构造并返回响应
        return Response(resp.content)

    except Exception as e:
        # Python 2 的异常处理
        return "Proxy Error: %s" % str(e), 500


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

    new_connection = params.get('newConnection', False)

    request_method = params.get('method', 'get')

    if new_connection:
        request_func = getattr(requests, request_method.lower())
    else:
        request_func = getattr(session, request_method.lower())

    resp = request_func(url, headers=headers, proxies=proxies, params=query, data=data, json=json, verify=False, cookies=cookies, timeout=timeout)

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
