# ライブラリをインポート
import numpy as np
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium import webdriver
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ホテル名やプラン名を格納する変数を用意
options = Options()
options.add_argument('--headless')
hotels_name = []
hotels_price = []
plan_name = []
geter_date = []
hotel_header = []
week = range(32)

# スクレイピングする元のページのurl
driver = webdriver.Chrome('doriver_path', chrome_options=options)
url_nagomi = 'https://www.jalan.net/yad321124/plan/?screenId=UWW3001&yadNo=321124&smlCd=260208&distCd=01&ccnt=yads2'
url_kawaramachi = 'https://www.jalan.net/yad319955/plan/?screenId=UWW3001&yadNo=319955&smlCd=260205&distCd=01&ccnt=yads2'
url_mystays = 'https://www.jalan.net/yad360286/plan/?screenId=UWW3001&stayCount=1&yadNo=360286&dateUndecided=1&roomCount=1&roomCrack=200000&adultNum=2&callbackHistFlg=1&smlCd=260208&distCd=01&ccnt=yads2'
url_hotel_gracery = 'https://www.jalan.net/yad302248/plan/?screenId=UWW3001&yadNo=302248&smlCd=260205&distCd=01&ccnt=yads2'
date = datetime.date.today()
actions = ActionChains(driver)


# ページをスクレイピング
def main(url=url_hotel_gracery):
    driver.get(url)
    header = driver.find_element_by_id('yado_header_hotel_name')
    hotel_header.append(header.text)
    time.sleep(5)
    check_box = driver.find_element_by_id('datecheck')
    check_box.click()
    date_box = driver.find_element_by_id('dyn_d_txt')
    date_box.clear()
    adlut = driver.find_element_by_id('dyn_adult_num')
    select = Select(adlut)
    select.select_by_index('2')
    if url == url_mystays:
        select.select_by_index('1')
    else:
        pass

    first_hotel_name = driver.find_element_by_id('yado_header_hotel_name')
    hotels_name.append(first_hotel_name.text)

    for days in week:
        time.sleep(3)
        date_box = driver.find_element_by_id('dyn_d_txt')
        date_box.clear()
        d = date + datetime.timedelta(days=days)
        time.sleep(3)
        date_box.send_keys(d.day)

        monyh_box = driver.find_element_by_id('dyn_m_txt')
        monyh_box.clear()
        monyh_box.send_keys(d.month)

        time.sleep(2)
        driver.find_element_by_id('research').click()
        time.sleep(3)

        first_hotel_price = driver.find_elements_by_class_name('p-searchResultItem__total')
        for i in first_hotel_price:
            hotels_price.append(i.text)
            if d.day == d.day:
                geter_date.append(d)

        element = driver.find_elements_by_css_selector(
            'td.p-searchResultItem__planNameCell > div.p-searchResultItem__planNameAndHorizontalLabels > a')
        for p in element:
            plan_name.append(p.text)

    time.sleep(3)
    print('終了')
    driver.quit()


# ~円になってるので取り除く
def replace_price(hotels_price):
    price_str = [int(s.replace('円', '').replace(',', '')) for s in hotels_price]
    return np.array(price_str).reshape(-1, 1)


# データフレームの作成とCSVの出力
def data_frame(replace_price, geter_date, plan_name):
    df = pd.DataFrame(data=replace_price(hotels_price), columns=['price'])
    df.insert(0, 'room_type', plan_name)
    df.insert(0, 'date', geter_date)
    print(df.head())
    df.to_csv('jaran_{a}_{b}.csv'.format(a=hotel_header[0], b=datetime.date.today()))
    if df.empty:
        print('空室なし')
    else:
        pass


if __name__ == '__main__':
    main()
    replace_price(hotels_price)
    data_frame(replace_price, geter_date, plan_name)
