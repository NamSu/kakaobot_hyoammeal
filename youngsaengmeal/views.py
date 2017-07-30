# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json
import time
import datetime
from datetime import date

import logging

logger = logging.getLogger(__name__)


# Kakao GET ~/keyboard/ 요청에 반응
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['아침', '점심', '저녁', '내일 아침', '내일 점심', '내일 저녁']
    })


# csrf 토큰 에러 방지, POST GET에 Response
@csrf_exempt
def message(request):
    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    meal = received_json_data['content']
    kcal = received_json_data['content']

    # 나중엔 수정해야함.
    daystring = ["월", "화", "수", "목", "금", "토", "일"]
    today = datetime.datetime.today().weekday()

    nextdaystring = ["화", "수", "목", "금", "토", "일", "월"]

    today_date = datetime.date.today().strftime("%m월 %d일 ")
    tomorrow_date = date.fromtimestamp(time.time() + 60 * 60 * 24).strftime("%m월 %d일 ")

    if meal == '아침' or meal == '점심' or meal == '저녁':
        return JsonResponse({
            'message': {
                'text': today_date + daystring[today] + '요일 ' + meal + ' 메뉴입니다. \n \n' + kcal + crawl(request)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['아침', '점심', '저녁', '내일 아침', '내일 점심', '내일 저녁']
            }
        })
    if meal == '내일 아침' or meal == '내일 점심' or meal == '내일 저녁':
        return JsonResponse({
            'message': {
                'text': '[' + meal + '] \n' + tomorrow_date + nextdaystring[today] + '요일 급식 메뉴입니다. \n \n' + crawl(
                    request)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['아침', '점심', '저녁', '내일 아침', '내일 점심', '내일 저녁']
            }
        })


# message request 있을시 Crawl 작동
def crawl(request):
    from bs4 import BeautifulSoup
    from urllib.request import urlopen

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    meal = received_json_data['content']

    # 타학교에서 이용시 수정
    regioncode = 'jbe.go.kr'
    schulcode = 'P100000429'

    if meal == '아침' or meal == '내일 아침':
        sccode = 1
    if meal == '점심' or meal == '내일 점심':
        sccode = 2
    if meal == '저녁' or meal == '내일 저녁':
        sccode = 3

    # NEIS
    html = urlopen(
        'http://stu.' + regioncode + '/sts_sci_md01_001.do?schulCode=' + schulcode + '&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=' + str(
            sccode))
    source = html.read()
    html.close()

    # to use beautifulsoup4 & make utf-8, parse lxml
    soup = BeautifulSoup(source, "lxml", from_encoding='utf-8')

    # div_id="contents"안의 table을 모두 검색 후 td태그만 추출
    table_div = soup.find(id="contents")
    tables = table_div.find_all("table")
    menu_table = tables[0]
    td = menu_table.find_all('td')

    # 요일 import, 월요일 ~ 일요일 = 0~6
    today = datetime.datetime.today().weekday()

    # 월요일 ~ 일요일 = td[8] ~ td[14]
    if meal == '아침' or meal == '점심' or meal == '저녁':
        if today == 6:
            menu = '일요일은 급식이 제공되지 않습니다....'
        else:
            menu = td[today + 8]

    if meal == '내일 아침' or meal == '내일 점심' or meal == '내일 저녁':
        if today == 5:
            menu = '일요일은 급식이 제공되지 않습니다.... '
        elif today == 6:
            menu = td[8]
        else:
            menu = td[today + 9]

    # 파싱 후 쓰레기 값 제거
    menu = str(menu).replace('*', '').replace('<td', '').replace('<br/></td>', '').replace('</td>', '').replace(
        'class="textC last">', '').replace('class="textC">', '').replace('<br/>', '\n').replace('1.', '').replace('2.',
                                                                                                                  '').replace(
        '3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace(
        '9.', '').replace('10.', '').replace('11.', '').replace('12.', '').replace('13.', '').replace('14.',
                                                                                                      '').replace('15.',
                                                                                                                  '').replace(
        '1', '').replace(' ', '')

    if menu == '':
        menu = '밥이 없습니다. 급식이 없는 날일 수 있으니 확인 바랍니다.'

    return menu
