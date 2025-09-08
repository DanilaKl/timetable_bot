import os

from dotenv import load_dotenv


load_dotenv()

# BOT TOKEN
TOKEN = os.getenv('BOT_TOKEN', '')

# MONGO DB
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'bot_data')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USER = os.getenv('MONGO_USER', '')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
MONGO_COLLECTION = 'users'


# REDIS FOR FSM
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_USER = os.getenv('REDIS_USER', '')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
