from flask import Flask
from src.routes.Mongo import mongo_api

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(mongo_api)

app.config['SECRET_KEY'] = 'secret!'

if __name__ == '__main__':
    port = 5001
    print('server run at:' + str(port))
    app.run(port=port)