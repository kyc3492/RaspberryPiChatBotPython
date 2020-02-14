#-*- coding: utf-8 -*-
import telepot, sys
from telepot.loop import MessageLoop
import Private

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if msg['text'] == '날씨':     #날씨라는 메시지가 도착했을 때 대답
            bot.sendMessage(chat_id, '맑았으면 좋겠습니다')
        else:                        #그 외에 다른 메시지가 도착했을 때 대답
            bot.sendMessage(chat_id, '무슨 말인지 모르겠군요')

TOKEN = Private.TOKEN    #Bot API 토큰

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# 프로그램을 계속 돌림
while True:
    input()
