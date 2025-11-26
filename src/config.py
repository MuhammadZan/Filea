import os, logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEBUG = True
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', '5000'))

# MongoDB connection using URI string (supports credentials)
# Set to None to disable MongoDB (file conversion doesn't require database)
MONGO_URI = os.getenv('MONGO_URI', None)
if MONGO_URI:
    MONGODB_SETTINGS = {
        'host': MONGO_URI,
    }

# File upload settings
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB default

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
