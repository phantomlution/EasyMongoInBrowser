# -*- coding:utf-8 -*-
import requests
from flask import Blueprint, request, Response
from utils.decorator import flask_response
from selenium import webdriver

selenium_api = Blueprint('selenium_api', __name__, url_prefix='/selenium')


@selenium_api.route('/cookie', methods=['POST'])
@flask_response
def resolve_cookie():
    params = request.get_json()
    url = params.get('url')

    driver = webdriver.Chrome()
    driver.implicitly_wait(1) # seconds
    driver.get(url)
    all_cookies = driver.get_cookies()
    user_agent = driver.execute_script("return navigator.userAgent;")
    driver.close()
    return {
        'ua': user_agent,
        'cookieList': all_cookies
    }
