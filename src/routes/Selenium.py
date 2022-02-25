# -*- coding:utf-8 -*-
from flask import Blueprint, request, Response
from utils.decorator import flask_response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")


selenium_api = Blueprint('selenium_api', __name__, url_prefix='/selenium')


@selenium_api.route('/cookie', methods=['POST'])
@flask_response
def resolve_cookie():
    params = request.get_json()

    url = params.get('url')

    sleep = params.get('sleep', 1)

    strategy = params.get('strategy', '')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(url)

    # seleniumDefense: try for extra time
    if strategy == 'seleniumDefense':
        time.sleep(0.1)
        driver.get(url)

    time.sleep(sleep)

    all_cookies = driver.get_cookies()

    user_agent = driver.execute_script("return navigator.userAgent;")

    driver.close()

    return {
        'ua': user_agent,
        'cookieList': all_cookies
    }
