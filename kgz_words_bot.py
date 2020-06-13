import telebot
import sqliter
from telebot import types

bot = telebot.TeleBot("1079116810:AAFKRqfx1XQhj6wG5jDifUUiHWsjtNpEpA4")

# @bot.message_handler(commands=['start'])
# def welcome(message):
#     bot.send_message(message.chat.id,
#                      "Привет\n*kgz words bot* - Собирает аудио файлы \n Чтобы зарегистрироваться нажмите на /login".format(
#                          message.from_user, bot.get_me()),
#                      parse_mode='html', reply_markup=None)
#     bot.register_next_step_handler(message, login)
#
# @bot.message_handler(commands=['login'])
# def login(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item1 = types.InlineKeyboardButton("Male", callback_data='male')
#     item2 = types.InlineKeyboardButton("Female", callback_data='female')
#
#     markup.add(item1, item2)
#
#     bot.send_message(message.chat.id, 'Выберите гендер?', reply_markup=markup)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == 'male':
#                 bot.send_message(call.message.chat.id, "М")
#             elif call.data == 'female':
#                 bot.send_message(call.message.chat.id, "Ж")
#
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ваш гендер:",
#                                   reply_markup=None)
#             bot.send_message(call.message.chat.id, 'Ваш возраст?')
#
#
#     except Exception as e:
#         print(repr(e))

# @bot.message_handler(content_types=['text'])
# def age(message):
#     global age
#     while age == 0:  # проверяем что возраст изменился
#         try:
#             age = int(message.text)  # проверяем, что возраст введен корректно
#         except Exception:
#             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

name = ''
surname = ''
age = 0


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Привет\n*kgz words bot* - Собирает аудио файлы \n Press /login".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=None)
    print(message.from_user)
@bot.message_handler(commands=['login'])
def login(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Male", callback_data='male')
    item2 = types.InlineKeyboardButton("Female", callback_data='female')

    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Выберите гендер?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'male':
                bot.send_message(call.message.chat.id, "М")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Ваш гендер:",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, 'Ваш возраст?')
            elif call.data == 'female':
                bot.send_message(call.message.chat.id, "Ж")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Ваш гендер:",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, 'Ваш возраст?')
            elif call.data == 'yes':
                bot.send_message(call.message.chat.id, "ok")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Age",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, 'asdasdfas?')
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, "repeat again")
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="age",
                                      reply_markup=None)
                bot.send_message(call.message.chat.id, 'gwehhbdas?')



    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['text'])
def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Да", callback_data='yes')
    item2 = types.InlineKeyboardButton("Нет", callback_data='no')

    markup.add(item1, item2)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + message.from_user.first_name + '?'
    bot.send_message(message.from_user.id, text=question,reply_markup=markup)


# RUN
bot.polling(none_stop=True)
