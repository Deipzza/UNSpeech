import os
from dotenv import load_dotenv

##Token
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'simple-bot/.env'))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

##Url
URL="https://simple-bot-e2ix-st3b.onrender.com"