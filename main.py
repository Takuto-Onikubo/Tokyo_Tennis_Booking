# <使い方>
# Park =        の後に「''」で囲んで公園名を、
# Month =       の後に月を、
# Day =         の後に日にちを入れる
# 利用開始時間はhour={}のカッコ内に「,」で区切って入れる。
# (他はいじらない)

Park = '舎人公園'
Year = 2022
Month = 8
Day = 15
hour = {17}
###ここまでを変える、ここから先はいじらない

surface = 'テニス（人工芝）'
if (Park == '大井埠頭公園'):
    surface = 'テニス（ハード）'

import requests
from bs4 import BeautifulSoup

PARK = '''\
日比谷公園: 1000
猿江恩賜公園: 1040
浮間公園: 1100
舎人公園: 1140
篠崎公園: 1150
木場公園: 1060
光が丘公園: 1190
井の頭公園: 1220
大井埠頭公園: 1310\
'''
park = dict([tuple(line.split(': ')) for line in PARK.split('\n')])

BODY = '''\
layoutChildBody:childForm:itemindex: 0
layoutChildBody:childForm:emptyStateKind: 1
layoutChildBody:childForm:eyear: 2025
layoutChildBody:childForm:offset: 0
layoutChildBody:childForm:allCount: 2
layoutChildBody:childForm:imstCCdItemsSave: 
layoutChildBody:childForm:layoutRsvMenu:viewName: RsvEmptyStatePage
layoutChildBody:childForm/view/user/rsvEmptyState.html: layoutChildBody:childForm
layoutChildBody:childForm:doChangeDate: submit\
'''
body = dict([tuple(line.split(': ')) for line in BODY.split('\n')])
body['layoutChildBody:childForm:bcd'] = park[Park]
body['layoutChildBody:childForm:year'] = Year
body['layoutChildBody:childForm:month'] = Month
body['layoutChildBody:childForm:day'] = Day

headers = {}
url = 'https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/rsvEmptyState.html'
def req(cookie):
    headers['Cookie'] = cookie
    response = requests.post(url=url, params=body, headers=headers, timeout=3)
    cookie = response.headers['Set-Cookie']
    return response.text, cookie

# 1回だけ空のCookieでリクエストを送りCookieを取得する
def main(event,context):
    _, cookie = req('')

    text, cookie = req(cookie)
    soup = BeautifulSoup(text, "html.parser")
    tmp = soup.find('div', id = 'isNotEmptyPager').find_all('table', class_ = 'tablebg2')
    num = []
    for tmp_ in tmp:
        if (tmp_.find('span', id = 'ppsname').contents[0] == surface):
            num = tmp_.find_all('span', id = 'emptyFieldCnt')
    t = 7

    #LINEで通知
    url_base = "https://notify-api.line.me/api/notify"
    access_token = 'KfiZu5lr3VPnLp6iL9DEa8LwCRGZ8VnU2zSybf8SVOj'
    headers_LINE = {'Authorization': 'Bearer ' + access_token}
    if (num == []):
        message = str(Month)+'月'+str(Day)+'日'+Park+'の予約でエラー'
        payload = {'message': message}
        r = requests.post(url_base, headers=headers_LINE, params=payload)

    for raw in num:
        t += 2
        vct = raw.contents
        if (vct[0] != '0' and t in hour):
            message = Park +'で'+str(Month)+'月'+str(Day)+'日'+str(t)+'時〜'+str(t+2)+'時に'+ vct[0] + '面空きがあります。'
            payload = {'message': message}
            r = requests.post(url_base, headers=headers_LINE, params=payload)