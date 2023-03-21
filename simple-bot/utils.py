from telebot import types

def gen_markup(menu):
  markup = types.InlineKeyboardMarkup()
  
  for item in menu:
    markup.add(types.InlineKeyboardButton(item["name"], callback_data=item["value"]))

  return markup