import socket

from telebot import types
from bot_functions.directory import *
from bot_functions.groups import *

def gen_markup(menu):
  markup = types.InlineKeyboardMarkup()
  
  for item in menu:
    markup.add(types.InlineKeyboardButton(item["name"], callback_data=item["value"]))

  return markup

def requests_directorio_handler(message, bot):
    metadata = message.text.split()
    response = select_query_directorio(metadata, "allunbot.db")
    if len(response) > 4095:
        for part in range(0, len(response), 4095):
            bot.send_message(message.chat.id, response[part:part+4095])
    else:
        bot.send_message(message.chat.id, response)

def search_groups_handler(message, bot):
   subject_code = message.text
   groups = select_query_groups(subject_code, "allunbot.db")
   bot.send_message(message.chat.id, groups)

def add_groups_name_handler(message, bot):
   subject_code = message.text
   text = "Escribe el nombre del grupo de la asignatura."
   sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
   bot.register_next_step_handler(sent_msg, add_groups_link_handler, subject_code, bot)

def add_groups_link_handler(message, subject_code, bot):
   subject_name = message.text
   text = "Escribe el enlace del grupo de la asignatura."
   sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
   bot.register_next_step_handler(sent_msg, add_groups_handler, subject_code, subject_name, bot)

def add_groups_handler(message, subject_code, subject_name, bot):
   link = message.text
   insert_values_into_groups(subject_code, subject_name, link)
   bot.send_message(message.chat.id, "Grupo agregado.", parse_mode="Markdown")

def auth_user(message, bot):
   initial_login = f"""
Para poder obtener la información del SIA necesitamos que ingreses al link:
http://localhost:10000/login

Utiliza este token para poder autenticarte:
{message.chat.id}
Mantén tu token seguro y guárdalo en un lugar seguro, ya que puede ser utilizado por cualquiera para acceder.
   """
   bot.send_message(message.chat.id, initial_login, parse_mode = "Markdown")