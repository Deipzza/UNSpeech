from telebot import types

def gen_markup():
  markup = types.InlineKeyboardMarkup()
  markup.add(types.InlineKeyboardButton("Pregrado", callback_data="pregrado"),types.InlineKeyboardButton("Posgrado", callback_data="posgrado"))
  return markup