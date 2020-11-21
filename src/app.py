from flask import Flask
from src.routes.Mongo import mongo_api
from src.routes.Proxy import proxy_api

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(mongo_api)
app.register_blueprint(proxy_api)

app.config['SECRET_KEY'] = 'secret!'

if __name__ == '__main__':
    port = 5001
    print('server run at:' + str(port))
    app.run(port=port, host='0.0.0.0')