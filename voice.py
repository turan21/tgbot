import sqlite3
import time
import telepot
import shutil
import sqliter
from pathlib import Path
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space, \
    include_callback_query_chat_id


def write_db(username, file_path, age, gender, first_name):
    db = sqlite3.connect('users.db')
    cur = db.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL PRIMARY KEY, username INTEGER NOT NULL UNIQUE,file_path TEXT, age INTEGER, gender INTEGER, first_name TEXT,count INTEGER)""")
    db.commit()
    data_person_name = [(username, file_path, age, gender, first_name), ]
    cur.execute("SELECT user_id FROM users")
    cur.executemany('INSERT OR IGNORE INTO users(username, file_path, age, gender, first_name) VALUES (?,?,?,?,?)',
                    data_person_name)
    db.commit()


def get_count(username):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"""SELECT count from users
WHERE username = {username}""")
    count = cur.fetchone()[0]
    Foo.count[f'{username}'] = count


def update_count(count, username):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    cur.execute(f"""UPDATE users
SET count = {count}
WHERE username = {username};""")
    db.commit()


class Foo(object):
    CONST_NAME = {}
    USER_INFO = []
    gender = {}
    count = {}


age_list = [1, 2, 3, 4, 5, 6]


class Voice(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Voice, self).__init__(*args, **kwargs)
        self._id = 0
        sqliter.main()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor='chat', long=True)
        get_count(msg["from"]["id"])
        if content_type == 'voice':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подтвердить", callback_data='yes'),
                 InlineKeyboardButton(text="Отмена", callback_data='no'), ]
            ]
            )
            bot.sendMessage(chat_id, 'Прослушайте заново и подтвердите', reply_markup=keyboard)
            Foo.CONST_NAME[msg['from']['id']] = msg
            return None
        elif content_type == 'text':
            Foo.CONST_NAME[msg['from']['id']] = msg
            if msg['text'] == '/start':
                Foo.count[str(msg['from']['id'])] = 0
                update_count(Foo.count[str(msg['from']['id'])], msg['from']['id'])
                # update_count(0, int(msg['from']['id']))
                Path(f'/home/pc/PycharmProjects/tgbot/files/{msg["from"]["id"]}').mkdir(parents=True, exist_ok=True)
                bot.sendMessage(chat_id,
                                'Доброго времени суток! ' + msg['from']['first_name'] + '\n Зарегистрируйтесь /reg')
            elif msg['text'] == '/reg':
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Мужской", callback_data='male'),
                     InlineKeyboardButton(text="Женский", callback_data='female'), ]
                ]
                )
                bot.sendMessage(chat_id, "Выберите ваш пол", reply_markup=markup)
            elif msg['text'] == '/next':
                if Foo.count[str(msg['from']['id'])] < len(sqliter.Words.WORDS_LIST) - 1:
                    Foo.count[str(msg['from']['id'])] += 1
                    update_count(Foo.count[str(msg['from']['id'])], str(msg['from']['id']))
                    bot.sendMessage(chat_id,
                                    str(sqliter.Words.WORDS_LIST[Foo.count[str(msg['from']['id'])]]).strip("()'',"))
                else:
                    bot.sendMessage(chat_id, "Подождите пока загрузим новые слова!\n try again later")
            elif msg['text'] == '/help':
                bot.sendMessage(chat_id, "Регистрация - /reg\n Начать упражнения - /exercise \n Инструкция - /help")
            elif msg['text'] == '/exercise':
                text = str(sqliter.Words.WORDS_LIST[Foo.count[str(msg['from']['id'])]]).strip("()'',")
                bot.sendMessage(chat_id, text)
            else:
                bot.sendMessage(chat_id, "Регистрация - /reg\n Начать упражнения - /exercise \n Инструкция - /help")

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(Foo.CONST_NAME[msg['from']['id']],
                                                                            flavor='chat', long=True)
        if query_data == 'yes':
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Отправлено")
            duration = Foo.CONST_NAME[msg['from']['id']]['voice']['duration']
            if duration > 30:
                bot.sendMessage(chat_id, ">30 секунд")
                return
            file_name = Foo.CONST_NAME[msg['from']['id']]['voice']['file_id']
            bot.download_file(Foo.CONST_NAME[msg['from']['id']]['voice']['file_id'], "{0}.ogg".format(file_name))
            my_file = Path("./{0}.ogg".format(Foo.CONST_NAME[msg['from']['id']]['voice']['file_id']))
            while not my_file.is_file():
                time.sleep(2)
            start_time = time.time()
            elapsed_time = time.time() - start_time
            print("Time Elapsed: ", elapsed_time)
            shutil.move(f'/home/pc/PycharmProjects/tgbot/{my_file}',
                        f'/home/pc/PycharmProjects/tgbot/files/{msg["from"]["id"]}/{my_file}')
        elif query_data == 'no':
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Запишите заново")
        elif query_data == 'male':
            Foo.gender[msg['from']['id']] = 0
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="6-12", callback_data=1),
                 InlineKeyboardButton(text="12-18", callback_data=2)], ])
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Сколько вам лет?",
                                reply_markup=markup)
        elif query_data == 'female':
            Foo.gender[msg['from']['id']] = 1
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="6-12", callback_data=1),
                 InlineKeyboardButton(text="12-18", callback_data=2)], ])
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Сколько вам лет?",
                                reply_markup=markup)
        elif int(query_data) in age_list:
            write_db(Foo.CONST_NAME[msg['from']['id']]['from']['id'],
                     f'/home/pc/PycharmProjects/tgbot/files/{Foo.CONST_NAME[msg["from"]["id"]]["from"]["id"]}',
                     query_data, Foo.gender[msg['from']['id']],
                     Foo.CONST_NAME[msg['from']['id']]['from']['first_name'])
            bot.editMessageText((msg['from']['id'], msg['message']['message_id']), "Регистрация прошла успешно")

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
