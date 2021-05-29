# -*- coding:utf-8 -*-
from flask import Flask, request
from routes.Mongo import mongo_api
from routes.Proxy import proxy_api
from routes.Selenium import selenium_api

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(mongo_api)
app.register_blueprint(proxy_api)
app.register_blueprint(selenium_api)

app.config['SECRET_KEY'] = 'secret!'


# fix large request body cause connection reset
@app.before_request
def handle_chunking():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True


if __name__ == '__main__':
    port = 5001
    print('server run at:' + str(port))
    app.run(port=port, host='0.0.0.0')