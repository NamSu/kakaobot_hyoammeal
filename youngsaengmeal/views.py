# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json
from datetime import *
from dateutil.relativedelta import *

import logging
logger = logging.getLogger(__name__)

# GET ~/keyboard/ 요청에 반응
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['오늘 급식', '내일 급식', '다른 요일 급식']
    })

# csrf 토큰 에러 방지, POST 요청에 message response
@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    meal = received_json_data['content']

    daystring = ["월", "화", "수", "목", "금", "토", "일"]
    nextdaystring = ["화", "수", "목", "금", "토", "일", "월"]

    today = date.today().weekday()
    today_date = date.today()
    tomorrow_date = today_date+relativedelta(days=+1)
    if meal in daystring:
        if today == 6:
            days = today_date + relativedelta(weekday=daystring.index(meal))
        else:
            days = today_date + relativedelta(days=-today, weekday=daystring.index(meal))

    if meal == '오늘 급식':
        return JsonResponse({
            'message': {
                'text': '[' + meal + '] \n' + today_date.strftime("%m월 %d일 ") + daystring[today] + '요일 급식입니다. \n' + read_txt(meal, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 급식', '내일 급식', '다른 요일 급식']
            }
        })
    elif meal == '내일 급식':
        return JsonResponse({
            'message': {
                'text': '[' + meal + '] \n' + tomorrow_date.strftime("%m월 %d일 ") + nextdaystring[today] + '요일 급식입니다. \n' + read_txt(meal, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 급식', '내일 급식', '다른 요일 급식']
            }
        })
    elif meal == '다른 요일 급식':
        return JsonResponse({
            'message': {
                'text': '급식정보가 필요한 요일을 입력해주세요.\n입력 가능 요일 : 월 화 수 목 금 토'
            },
            'keyboard': {
                'type': 'text'
            }
        })
    elif meal in daystring and meal != "일":
        return JsonResponse({
            'message': {
                'text': days.strftime("%m월 %d일 ") + meal + '요일 급식입니다. \n \n' + read_txt(meal, today, daystring)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['오늘 급식', '내일 급식', '다른 요일 급식']
            }
        })
    else:
        return JsonResponse({
            'message': {
                'text': '잘못된 입력입니다. ' + '[' + meal + ']' + '\n입력 가능 명령어 : 월 화 수 목 금 토'
            },
            'keyboard': {
                'type': 'text'
            }
        })

def read_txt(meal, today, daystring):
    # 0(월요일) ~ 5(토요일).txt read
    if meal == '오늘 급식':
        f = open(str(today) + ".txt", 'r')
    if meal == '내일 급식':
        if today == 6:
            f = open("0.txt", 'r')
        else:
            today = today + 1
            f = open(str(today) + ".txt", 'r')
    if meal in daystring:
        f = open(str(daystring.index(meal)) + ".txt", 'r')
    menu = f.read()
    f.close()

    return menu