import telebot
from telebot import types


bot=telebot.TeleBot("1079116810:AAFKRqfx1XQhj6wG5jDifUUiHWsjtNpEpA4")
#
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id,"Сколько вам лет?")
        bot.register_next_step_handler(message,get_age)
    else:
        bot.send_message(message.from_user.id,'Напишите "/reg"')
# def gender(message):
#     bot.send_message(message.from_user.id, "Выберите пол")
#     keyboard = types.InlineKeyboardMarkup()
#     key_male = types.InlineKeyboardButton(text='Мужской', callback_data='male')
#     keyboard.add(key_male)
#     key_female = types.InlineKeyboardButton(text='Женский', callback_data='female')
#     keyboard.add(key_female)
#     bot.register_next_step_handler(message, get_age)
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "male":
#         bot.send_message(call.message.chat.id,"Man")
#     elif call.data == "female":
#         bot.send_message(call.message.chat.id, "Woman")
def get_age(message):
    global age
    age = int(message.text)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + message.from_user.first_name + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Ok')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Напишите "/reg"')

bot.polling(none_stop=True, interval=0)
