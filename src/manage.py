from flask import Flask
from flask.ext.script import Manager

import config
from model.abc import db

server = Flask(__name__)
server.debug = config.DEBUG
server.config['MONGODB_SETTINGS'] = config.MONGODB_SETTINGS
db.init_app(server)

manager = Manager(server)

# MongoDB doesn't require migrations like SQL databases
# You can add custom commands here if needed

if __name__ == '__main__':
    manager.run()
