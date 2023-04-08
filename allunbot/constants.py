import os
from dotenv import load_dotenv

# Bot token
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'allunbot/.env'))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# URL
URL = os.environ.get("URL")

# MongoDB
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")