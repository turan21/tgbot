import time,telepot
from pathlib import Path
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space,per_callback_query_chat_id,include_callback_query_chat_id

class Voice(telepot.helper.ChatHandler):
    def __init__(self,*args, **kwargs):
        super(Voice,self).__init__(*args, **kwargs)
        self._id = 0

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, flavor='chat', long=True)

        if content_type == 'voice':
            duration = msg['voice']['duration']
            if(duration)>30:
                bot.sendMessage(chat_id, ">30 секунд")
                return
            file_name = msg['voice']['file_id']
            bot.download_file(msg['voice']['file_id'], "{0}.ogg".format(file_name))
            my_file = Path("./{0}.ogg".format(msg['voice']['file_id']))

            while not my_file.is_file():
                time.sleep(2)

            start_time = time.time()
            elapsed_time = time.time() - start_time
            print("Time Elapsed: ", elapsed_time)
            # bot.sendVoice(chat_id, open(file_name + '.mp3', 'rb'))
            return None
        elif content_type == 'text':
            if msg['text'] == '/start':
                bot.sendMessage(chat_id,'Hi! '+msg['from']['first_name']+'\n /reg')
            elif msg['text'] == '/reg':
                bot.sendMessage(chat_id,"/\/\/\/")
            elif msg['text'] == '/my':
                bot.sendMessage(chat_id,msg['from'])
            elif msg['text'] == '/help':
                bot.sendMessage(chat_id,"registration - /reg\n \n my information - /my\n \n help - /help")
            else:
                bot.sendMessage(chat_id, "registration - /reg\n \n my information - /my\n \n help - /help")

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