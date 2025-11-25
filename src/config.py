import os, logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG = True
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', '5000'))

MONGODB = {
    'host': os.getenv('MONGODB_HOST', os.getenv('DB_PORT_27017_TCP_ADDR', 'localhost')),
    'port': os.getenv('MONGODB_PORT', os.getenv('DB_PORT_27017_TCP_PORT', '27017')),
    'db': os.getenv('MONGODB_DB', 'filea'),
}
MONGODB_SETTINGS = {
    'host': MONGODB['host'],
    'port': int(MONGODB['port']),
    'db': MONGODB['db'],
}

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
