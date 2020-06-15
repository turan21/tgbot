import time, telepot
import os, shutil
from pathlib import Path
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space, per_callback_query_chat_id, \
    include_callback_query_chat_id


class Foo(object):
    CONST_NAME = ""


class Voice(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Voice, self).__init__(*args, **kwargs)
        self._id = 0

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor='chat', long=True)
        if content_type == 'voice':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подтвердить", callback_data='yes'),
                 InlineKeyboardButton(text="Отмена", callback_data='no'), ]
            ]
            )
            bot.sendMessage(chat_id, 'Прослушайте заново и подтвердите', reply_markup=keyboard)
            Foo.CONST_NAME = msg
            return None
        elif content_type == 'text':
            if msg['text'] == '/start':
                bot.sendMessage(chat_id, 'Privet! ' + msg['from']['first_name'])
                print(msg)
            elif msg['text'] == '/reg':
                bot.sendMessage(chat_id, "Registration")
            elif msg['text'] == '/my':
                bot.sendMessage(chat_id, msg['from']['first_name'])
            elif msg['text'] == '/my':
                bot.sendMessage(chat_id, msg['from']['first_name'])
            elif msg['text'] == '/help':
                bot.sendMessage(chat_id, "registration - /reg\n my name - /my\n help - /help")
            else:
                bot.sendMessage(chat_id, "registration - /reg\n my name - /my\n help - /help")

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(Foo.CONST_NAME, flavor='chat', long=True)
        if query_data == 'yes':
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Отправлено")
            duration = Foo.CONST_NAME['voice']['duration']
            if duration > 30:
                bot.sendMessage(chat_id, ">30 секунд")
                return

            file_name = Foo.CONST_NAME['voice']['file_id']
            bot.download_file(Foo.CONST_NAME['voice']['file_id'], "{0}.ogg".format(file_name))
            my_file = Path("./{0}.ogg".format(Foo.CONST_NAME['voice']['file_id']))

            while not my_file.is_file():
                time.sleep(2)

            start_time = time.time()
            elapsed_time = time.time() - start_time
            print("Time Elapsed: ", elapsed_time)
            shutil.move(f'/home/pc/PycharmProjects/tgbot/{my_file}', f'/home/pc/PycharmProjects/tgbot/files/{my_file}')
        elif query_data == 'no':
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Запишите заново")


bot = telepot.DelegatorBot("1079116810:AAFKRqfx1XQhj6wG5jDifUUiHWsjtNpEpA4", [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(), create_open, Voice, timeout=90)
])
MessageLoop(bot).run_as_thread()
answerer = telepot.helper.Answerer(bot)
print('Listening ...')

while 1:
    time.sleep(10)
