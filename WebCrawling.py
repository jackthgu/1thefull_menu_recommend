

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib

## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe',chrome_options=options)
driver.implicitly_wait(3)

with urllib.request.urlopen('http://api.fooding.io/search?price=&week=&time=&headcount=&filter_list=&type=1&search_content=') as url:
    data = json.loads(url.read().decode())

driver.get('http://www.fooding.io/after-filter?week=&time=&headcount=&type=1&search_content=')
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

p = re.compile('^(\d+[a-z])')
p1 = re.compile('(\w+\(?\w+\)?)')
p2 = re.compile('(\d+)')
##3요놈으로 하면 되겠네
name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량

for i in range(len(data['product_list'])):
    name.append(data['product_list'][i]['item_name'])
    if data['product_list'][i]['sale_price'] == None:
        price.append(data['product_list'][i]['price'])
    else:
        price.append(data['product_list'][i]['sale_price'])

for i in range(len(data['product_list'])):
    while (1):
        food_id = data['product_list'][i]['item_id']
        driver.get('http://www.fooding.io/detail/' + str(food_id) + '/1')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        bb = soup.findAll('span', {'class': 'value'})[2].get_text()
        cc = soup.findAll('span', {'class': 'value'})[3].get_text()
        if len(p1.findall(cc)) == 0:
            pass
        else:
            weight.append(int(p2.findall(cc)[0]))
            material.append(p1.findall(bb))
            break

## 만약 재료와 원산지를 따로 구분하고 싶다면
aa = material[0]
origin = [x.split('(')[1].replace(')', '') for x in aa]  ## 괄호 안에 있는 단어 추출
material_only = [x.split('(')[0] for x in aa]  ## 괄호 왼쪽에 있는 단어 추출

print(name)
print(price)
print(nutrient)
print(material)
print(weight)
print(origin)
print(material_only)
