from flask import Flask
from flask.ext.cors import CORS

import config
from model.abc import db

server = Flask(__name__)
server.debug = config.DEBUG

server.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
db.init_app(server)

CORS(
    server,
    resources={r"/*": {"origins": "*"}},
    headers=['Content-Type', 'X-Requested-With', 'Authorization']
)

from route.common import common_blueprint
server.register_blueprint(common_blueprint)


if __name__ == '__main__':
    server.run(host=config.HOST, port=config.PORT)
