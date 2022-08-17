from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from time import sleep
import pandas as pd

#csvファイルの開始列と終了列
sta=2
fin=90


url = 'https://yoyaku.sports.metro.tokyo.lg.jp/user/view/user/rsvEmptyState.html'

def lottery(Park, day, hour, userid, password, list):
    #seleniumの設定
    # スパム認識されないようにランダムにスリープを挟む  
    options = Options()
    options.add_argument('--headless') #ヘッダーレスにしない時はコメントアウト
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    sleep(0.2)
    browser.find_element_by_id('login').click()
    sleep(1.2)
    browser.find_element_by_id('userid').send_keys(userid)
    sleep(1.8)
    browser.find_element_by_id('passwd').send_keys(password)
    sleep(0.4)
    browser.find_element_by_id('login').click()
    sleep(0.3)
    browser.find_element_by_id('goLotSerach').click()
    sleep(0.2)
    browser.find_elements_by_id('clscd')[3].click()
    sleep(0.4)
    browser.find_element_by_id('doSearch').click()
    sleep(0.3)
    for i in range(3):
        PARKS = browser.find_elements_by_id('bgcdnamem')
        parks = [i.text for i in PARKS]
        cnt = 0
        for park in parks:
            if park == Park:
                browser.find_elements_by_id('doAreaSet')[cnt].click()
                sleep(0.3)
                browser.find_elements_by_class_name('calclick')[day-1].click()
                sleep(0.2)
                browser.find_elements_by_id('selectKom')[(hour-9)//2].click()
                sleep(0.3)
                browser.find_element_by_id('doDateTimeSet').click()
                sleep(0.4)
                browser.find_element_by_id('doOnceFix').click()
                sleep(0.4)
                Alert(browser).accept()
                sleep(0.3)
                browser.find_element_by_id('doDateSearch').click()
                sleep(0.2)
                browser.find_elements_by_class_name('calclick')[day-1].click()
                sleep(0.3)
                browser.find_elements_by_id('selectKom')[(hour-9)//2].click()
                sleep(0.4)
                browser.find_element_by_id('doDateTimeSet').click()
                sleep(0.2)
                browser.find_element_by_id('doOnceFix').click()
                sleep(0.5)
                Alert(browser).accept()
                sleep(0.2)
                print(str(sta)+": "+str(list)+'予約完了')
                return()
            else:
                cnt += 1
        browser.find_element_by_id('goNextPager').click()
        sleep(0.6)

data = pd.read_csv('抽選04.csv',usecols=[1, 2, 6, 10, 11], dtype={'カード番号':'object', 'パスワード':'object', '時間帯':'object'})
chusen_list=[]
for i in range(sta-2, fin-1):
    num = data['カード番号'][i]
    pas = data['パスワード'][i]
    park = data['抽選にかけた場所'][i]
    if park == '猿江':
        park = '猿江恩賜公園'
    elif park == '舎人':
        park = '舎人公園'
    elif park == '日比谷':
        park = '日比谷公園'
    elif park == '井の頭':
        park = '井の頭恩賜公園'
    elif park == '篠崎':
        park = '篠崎公園Ａ'
    elif park == '木場':
        park = '木場公園'
    elif park == '城北':
        park = '城北中央公園Ａ'
    time = data['時間帯'][i]
    if time == '9-11':
        time = int(9)
    elif time == '11-13':
        time = int(11)
    elif time == '13-15':
        time = int(13)
    elif time == '15-17':
        time = int(15)
    elif time == '17-19':
        time = int(17)
    elif time == '19-21':
        time = int(19)
    day = int(data['日付'][i])
    chusen_list.append([park, day, time, num, pas])

for place in chusen_list:
    try:
        lottery(*place, place)
    except:
        print(str(place)+'で抽選登録できませんでした。')
