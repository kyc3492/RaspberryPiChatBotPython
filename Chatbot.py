#-*- coding: utf-8 -*-
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
    isitRain = False
    isitSnow = False
    windDirArray = ["북", "북북동", "북동", "동북동", "동", "동남동", "남동", "남남동", "남", "남남서", "남서", "서남서", "서", "서북서", "북서", "북북서", "북"]
    VVV = 0.0
    UUU = 0.0
    windSpd = 0
    fcstTime = 0

    now_time = now.strftime('%H')
    print(now_time)

    int_baseTime = int(now_time) - 2
    if(int_baseTime > 0):
        if(int_baseTime % 3 == 1):
            int_baseTime += 1
        elif(int_baseTime % 3 == 2):
            pass
        else:
            int_baseTime += 2
    else:
        int_baseTime = 23

    if(int_baseTime < 10):
        base_time = '0' + str(int_baseTime) + '00'
    else:
        base_time = str(int_baseTime) + '00'

    if(int(now_time) > 23 or int(now_time) < 3):
        yesterday_date = now - datetime.timedelta(1)
        now_date = yesterday_date.strftime('%Y%m%d')

    print(base_time)

    url_endpoint = Private.url_endpoint
    url_baseDate = 'base_date=' + now_date + '&'
    url_baseTime = 'base_time=' + base_time + '&'
    url_location = 'nx=' + '62' + '&' + 'ny=' + '122' + '&'
    url_numOfRows = 'numOfRows=10' + '&'
    url_pageNo = 'pageNo=1' + '&'
    url_dataType = '_type=json'
    url = url_endpoint + url_baseDate + url_baseTime + url_location + url_numOfRows + url_pageNo + url_dataType

    response = urlopen(url).read().decode('utf-8')
    responseJson = json.loads(response)
    completed_message = ""
    for i in responseJson["response"]["body"]["items"]["item"]:
        #completed_message += str(i["category"]) + " " + str(i["fcstValue"]) + "\n"
        if(str(i["category"]) == "POP"):
            completed_message += str(i["fcstTime"])[0:2] + "시에 예보된 강수확률은 " + str(i["fcstValue"]) + "%입니다. \n"
        elif(str(i["category"]) == "PTY" and i["fcstValue"] != 0):
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
        elif(str(i["category"]) == "R06" and isitRain == True):
            completed_message += "강수량은 " + str(i["fcstValue"]) + "mm입니다. \n"
        elif(str(i["category"]) == "S06" and isitSnow == True):
            completed_message += "적설량은 " + str(i["fcstValue"]) + "cm입니다. \n"
        elif(str(i["category"]) == "REH"):
            completed_message += "습도는 " + str(i["fcstValue"]) + "%입니다. \n"
        elif(str(i["category"]) == "SKY"):
            if(i["fcstValue"] == 1):
                completed_message += "하늘상태는 맑습니다. \n"
            elif(i["fcstValue"] == 2):
                completed_message += "하늘상태는 구름이 조금 있습니다. \n"
            elif(i["fcstValue"] == 3):
                completed_message += "하늘상태는 구름이 많습니다. \n"
            else:
                completed_message += "하늘상태는 흐립니다. \n"
        elif(str(i["category"]) == "T3H"):
            completed_message += "최근 3시간동안의 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        elif(str(i["category"]) == "TMN"):
            completed_message += "아침 최저 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        elif(str(i["category"]) == "TMX"):
            completed_message += "낮 최고 기온은 "+ str(i["fcstValue"]) + "℃입니다. \n"
        elif(str(i["category"]) == "VEC"):
            windDir = (i["fcstValue"] + 22.5 * 0.5) / 22.5
            completed_message += "풍향은 "+ windDirArray[int(windDir)] + "풍 입니다. \n"
        elif(str(i["category"]) == "WSD"):
        	completed_message += "풍속은 " + str(i["fcstValue"]) + "m/s입니다.\n"
        '''
        elif(str(i["category"]) == "UUU"):
            print(i["fcstValue"])
            if(i["fcstValue"] < 0):
                UUU = i["fcstValue"] - i["fcstValue"] * 2
            else:
                UUU = i["fcstValue"]
        elif(str(i["category"]) == "VVV"):
            print(i["fcstValue"])
            if(i["fcstValue"] < 0):
                VVV = i["fcstValue"] - i["fcstValue"] * 2
            else:
                VVV = i["fcstValue"]
            if(UUU >= 0):
                windSpd = VVV + UUU
                completed_message += "풍속은 " + str(round(windSpd, 1)) + "m/s입니다.\n"
        '''


    print(json.dumps(responseJson, indent=4))

    if content_type == 'text':
        if msg['text'] == '날씨':
            bot.sendMessage(chat_id, completed_message)
        else:
            bot.sendMessage(chat_id, '무슨 말인지 모르겠군요')


TOKEN = Private.TOKEN    # 텔레그램으로부터 받은 Bot API 토큰
#안드로이드 외부 편집 테스트

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while True:
    input()
