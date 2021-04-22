from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def return_url(word):
    url = "https://www.diningcode.com/isearch.php?query=" + word + " 카페"
    return url

def more_list(driver):
    more = driver.find_element_by_css_selector("#btn_normal_list > a")
    more.click()
    #time.sleep(3)

def more_btn(driver):
    btn = driver.find_element_by_css_selector("span.more-btn")
    btn.click()
    time.sleep(3)

def get_data(driver, i, word):
    tag = '#div_list > li[onmouseenter="setIcon(' + str(i) + ');"]'
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.select(tag)[0]
    
    store_name = content.select('.btxt')[0].text[3:].strip()
    main_food = content.select('.stxt')[0].text
    #features = content.select('.ctxt')[0].text
    try:
        loc_key = content.select('.ctxt > i.loca')[0].text
    except:
        loc_key = ''
    #loc_key = word
    locationall = content.select('span.ctxt:nth-of-type(odd)')[0].text
    location = locationall[len(loc_key):]
    like = int(content.select('.favor.button')[0].text)
    #grade = int(content.select('.point')[0].text[:-1]) * 0.05
    imgtag = tag + " span.img"
    my_property = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, imgtag))).value_of_css_property("background-image")
    img_url = re.split('[()]',my_property)[1][1:-1]
    #data = [store_name, main_food, features, loc_key, location, like, grade, img_url]
    data = [store_name, word, location, main_food, like, img_url]
    return data

    
def crawling(driver, word, count, arr):
    url = return_url(word)                  # word = 검색할 키워드
    driver.get(url)                         #사이트로 이동
    time.sleep(5)                           #페이지 로드될때까지 기다리기
    
    more_list(driver)                       #더보기버튼 누르기
    time.sleep(5)                           #페이지 로드될때까지 기다리기

    for idx in range(1, count+1):
        results.append(get_data(driver, idx, word))
        if(idx % 10 == 0): 
            more_btn(driver)


driver = webdriver.Chrome('C:/python-workspace/chromedriver.exe') 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

#word_list = ['홍대', '이태원']
word_list = ['홍대', '이태원', '가로수길', '연남동', '잠실', '청담', '압구정', '합정', '건대', '성수동', '을지로', '한남동', '여의도','논현동','영등포','왕십리','대학로','인사동','삼청동','광화문', '명동', '강남역', '신도림', '사당', '동대문', '노원역', '성신여대', '연신내', '천호'] 

#word_list = ['홍대', '연남동', '이태원', '건대'] 
#word_list = ['신촌', '가로수길', '청담', '광화문']
#word_list = ['삼청동', '인사동', '한남동', '혜화']

results = []
count = 30      #각각 30개씩 크롤링

for word in word_list:
    crawling(driver, word, count, results)

#결과 csv로 저장
df = pd.DataFrame(results)
#df.columns = ['store_name', 'main_food', 'features', 'loc_key', 'location', 'like', 'grade', 'img_url']
#df.columns = ['restaurant_name', 'location_name', 'full_address', 'main_food', 'like', 'image']
df.columns = ['cafe_name', 'location_name', 'full_address', 'main_food', 'like', 'image']
df.to_csv("cafes_data.csv", header=True, index=None)

driver.close()