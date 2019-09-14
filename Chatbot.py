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
    isitRain = False;
    isitSnow = False;
    windDirArray = ["북", "북북동", "북동", "동북동", "동", "동남동", "남동", "남남동", "남", "남남서", "남서", "서남서", "서", "서북서", "북서", "북북서", "북"]

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
    completed_message = ""
    for i in responseJson["response"]["body"]["items"]["item"]:
        completed_message += str(i["category"]) + " " + str(i["fcstValue"]) + "\n"
        if(str(i["category"]) == "POP"):
            completed_message += "강수확률은 " + str(i["fcstValue"]) + "%입니다. \n"
        if(str(i["category"]) == "PTY" and str(i["fcstValue"]) == 0):
            if(str(i["fcstValue"]) == 1):
                completed_message += "강수형태는 비입니다. \n"
                isitRain = True
            elif(str(i["fcstValue"]) == 2):
                completed_message += "강수형태는 진눈개비입니다. \n"
                isitRain = True
                isitSnow = True
            elif(str(i["fcstValue"]) == 3):
                completed_message += "강수형태는 눈입니다. \n"
                isitSnow = True
            else:
                completed_message += "강수형태는 소나기입니다. \n"
                isitRain = True
        #GRIB처리 찾아볼 것
        if(str(i["category"]) == "REH"):
            completed_message += "습도는 " + str(i["fcstValue"]) + "%입니다. \n"
        if(str(i["category"]) == "SKY"):
            if(str(i["fcstValue"]) == 1):
                completed_message += "하늘상태는 맑습니다. \n"
            if(str(i["fcstValue"]) == 2):
                completed_message += "하늘상태는 구름이 조금 있습니다. \n"
            if(str(i["fcstValue"]) == 3):
                completed_message += "하늘상태는 구름이 많습니다. \n"
            if(str(i["fcstValue"]) == 4):
                completed_message += "하늘상태는 흐립니다. \n"
        if(str(i["category"]) == "T3H"):
            completed_message += "최근 3시간동안의 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        if(str(i["category"]) == "TMN"):
            completed_message += "아침 최저 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        if(str(i["category"]) == "TMX"):
            completed_message += "낮 최고 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        if(str(i["category"]) == "VEC"):
            windDir = (i["fcstValue"] + 22.5 * 0.5) / 22.5
            
        	
    print(json.dumps(responseJson, indent=4))
 
    if content_type == 'text':
        if msg['text'] == '날씨':
            bot.sendMessage(chat_id, completed_message)
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
