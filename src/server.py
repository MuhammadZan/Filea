from flask import Flask
from flask.ext.cors import CORS

import config
from model.abc import db

server = Flask(__name__)
server.debug = config.DEBUG

# Only initialize MongoDB if URI is provided
if hasattr(config, 'MONGO_URI') and config.MONGO_URI and 'mongodb' in config.MONGO_URI:
    server.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
    db.init_app(server)

CORS(
    server,
    resources={r"/*": {"origins": "*"}},
    headers=['Content-Type', 'X-Requested-With', 'Authorization']
)

from route.common import common_blueprint
server.register_blueprint(common_blueprint)

from route.conversion import conversion_blueprint
server.register_blueprint(conversion_blueprint, url_prefix='/api')


if __name__ == '__main__':
    server.run(host=config.HOST, port=config.PORT)
