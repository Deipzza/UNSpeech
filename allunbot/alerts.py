import schedule
import telebot
import datetime
import time

from constants import *

bot = telebot.TeleBot(BOT_TOKEN, threaded = False)
chat_id = '6158731448'
message = 'Hello, world!'
send_time = str(datetime.datetime(2023, 4, 25, 18, 46))[:16]  # Set the time to send the message
# send_time = datetime.date(2023, 4, 25)  # Set the time to send the message
print(send_time)


while True:
    now = str(datetime.datetime.now())[:16]
    print(now)
    if now >= send_time:
    # if datetime.date.today() >= send_time:
        bot.send_message(chat_id=chat_id, text=message)
        break
    print("not yet")
    time.sleep(2)  # Sleep for a minute and check again

def send_message():
    bot.send_message(chat_id=chat_id, text="aaaaa")

schedule.every().day.at('18:55').do(send_message)