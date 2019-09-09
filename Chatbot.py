#-*- coding: utf-8 -*-
import time
import telepot, sys
from telepot.loop import MessageLoop
from urllib import parse
from urllib.request import urlopen
import datetime
import json
import Private

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    now = datetime.datetime.now()
    now_date = now.strftime('%Y%m%d')
    print(now_date)

    now_time = now.strftime('%H')
    int_nowTime = int(now_time) - 2
    if(int_nowTime > 0):
        if(int_nowTime % 3 == 1):
            int_nowTime += 1
        elif(int_nowTime % 3 == 2):
            pass
        else:
            int_nowTime += 2
    else:
        int_nowTime = 23

    if(int_nowTime < 10):
        base_time = '0' + str(int_nowTime) + '00'
    else:
        base_time = str(int_nowTime) + '00'

    print(base_time)

    url_endpoint = Private.url_endpoint
    url_baseDate = 'base_date=' + now_date + '&'
    url_baseTime = 'base_time=' + base_time + '&'
    url_location = 'nx=' + '60' + '&' + 'ny=' + '126' + '&'
    url_numOfRows = 'numOfRows=10' + '&'
    url_pageNo = 'pageNo=1' + '&'
    url_dataType = '_type=json'
    url = url_endpoint + url_baseDate + url_baseTime + url_location + url_numOfRows + url_pageNo + url_dataType

    response = urlopen(url).read().decode('utf-8')
    responseJson = json.loads(response)

 
    if content_type == 'text':
        if msg['text'] == '날씨':
            bot.sendMessage(chat_id, responseJson)
        elif msg['text'] == '/start':
            pass
        elif msg['text'] == '/end':
            sys.exit(1)
        elif msg['text'] == '끝내자':
            bot.sendMessage(chat_id, '또 봅시다 휴먼')
        else:
            bot.sendMessage(chat_id, '무슨 말인지 모르겠군요')
 
 
TOKEN = Private.TOKEN    # 텔레그램으로부터 받은 Bot API 토큰
#안드로이드 외부 편집 테스트
 
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')
 
# Keep the program running.
while True:
    time.sleep(1000)
