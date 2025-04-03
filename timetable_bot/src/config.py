import os

from dotenv import load_dotenv


load_dotenv()

# BOT TOKEN
TOKEN = os.getenv('BOT_TOKEN', '')
