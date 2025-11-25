import os, logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG = True
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', '5000'))

# MongoDB connection using URI string (supports credentials)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/filea')
MONGODB_SETTINGS = {
    'host': MONGO_URI,
}

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
