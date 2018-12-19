### 푸딩에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import re
import json
import urllib
import os

## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

with urllib.request.urlopen(
        'http://api.fooding.io/search?price=&week=&time=&headcount=&filter_list=&type=1&search_content=') as url:
    data = json.loads(url.read().decode())

driver.get('http://www.fooding.io/after-filter?week=&time=&headcount=&type=1&search_content=')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

p = re.compile('^(\d+[a-z])')
p1 = re.compile('(\w+\(?\w+\)?)')
p2 = re.compile('(\d+)')
##3요놈으로 하면 되겠네
name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []  # 이미지 패스

for i in range(len(data['product_list'])):
    name.append(data['product_list'][i]['item_name'])
    if data['product_list'][i]['sale_price'] == None:
        price.append(data['product_list'][i]['price'])
    else:
        price.append(data['product_list'][i]['sale_price'])
    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/fooding/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    urllib.request.urlretrieve(data['product_list'][i]['image'][0]['img_url'], img_path)  # 음식이미지 폴더에 저장

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
            ## material.append(p1.findall(bb))
            material.append(','.join(p1.findall(bb)))
            break

## 만약 재료와 원산지를 따로 구분하고 싶다면
# aa = material[0]
# origin = [x.split('(')[1].replace(')','') for x in aa] ## 괄호 안에 있는 단어 추출
# material_only = [x.split('(')[0] for x in aa] ## 괄호 왼쪽에 있는 단어 추출

# print(name)
# print(price)
# print(nutrient)
# print(material)
# print(weight)
# print(origin)
# print(material_only)

food_dict_list = []
for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'fooding'
    temp['online_market_address'] = 'http://www.fooding.io'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = weight[i]
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = image_path[i]
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)

####################################################################################################################

### 더반찬에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p = re.compile('.*\{(.*)}.*')  ## {}안에 있는 문자들 모두 가져오기
p1 = re.compile('\d*\,*\d+\s*g')
## 음식에 대한 상세정보 페이지로 이동하기 위해 goods_no을 알아내는 코드
## url을 통한 html 가져오기 ##
driver.get('http://www.thebanchan.co.kr/dispctg/initDispCtg.action?disp_ctg_no=1707080302')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []  # 이미지 패스

## 더보기 클릭버튼을 이용하여 하위 정보 소스까지 받아야함

a = True
while (a):
    try:
        driver.find_element_by_id('gAddBtn').click()
    except:
        a = False
        break
    else:
        a = True

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

## url정보가 a태그에 있으므로 a태크로 이동
aa = soup.select('li > a')
bb = [x for x in aa if 'onclick' in x.attrs.keys()]

for i in range(len(bb)):
    cc = p.findall(bb[i]['onclick'])[0].replace(' ', '')  ## bb[0]을 bb[i]로 바꿔야 한다
    dd = cc.split(',')
    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/thebanchan/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    urllib.request.urlretrieve('https:' + bb[i].find('img')['src'], img_path)
    ## 딕셔너리 형태로 변환
    data = dict()
    for i in dd:
        s1 = i.split(':')
        data[s1[0]] = s1[1].replace("'", "")

    data['target'] = '_self'
    base = 'http://www.thebanchan.co.kr/goods/initGoodsDetail.action'
    params = data
    url = url_with_parameter(base, params)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 제품 이름
    name.append(soup.find('h2', {'class': 'gd_name'}).text)
    # 제품 가격
    # span 태그의 class 속성 값으로 sale을 갖는 하위태그 b에 담겨 있는 텍스트 출력
    temp = soup.find('span', {'class': 'sale'}).b.text
    # 텍스트 원단위를 int형으로 변환하여 price 배열에 넣기
    price.append(int(temp.replace(',', '')))
    # 음식재료

    # 중량
    if soup.select('tr > th')[5].text == '내용량':
        xx = soup.select('tr > td')[5].text
        material.append(soup.select('tr > td')[6].text)
    elif soup.select('tr > th')[3].text == '내용량':
        xx = soup.select('tr > td')[3].text
        material.append(soup.select('tr > td')[4].text)
    else:
        xx = soup.select('tr > td')[4].text
        material.append(soup.select('tr > td')[5].text)  ## 음식재료
    if 'kg' in xx:
        pp = re.compile('\d*\.*\d+')
        weight.append(int(pp.findall(xx)[0].replace(' ', '').replace('.', '')) * 1000)
    else:
        weight.append(int(p1.findall(xx)[0].replace(' ', '').replace(',', '').replace('g',
                                                                                      '')))  # 숫자+g 형태의 단어를 추출한다음 g을 지우고 int로 변환한다.
    # weight.append(xx)

food_dict_list = []
for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'thebanchan'
    temp['online_market_address'] = 'http://www.thebanchan.co.kr'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = weight[i]
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = image_path[i]
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)

####################################################################################################################

### 몽촌반찬에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p1 = re.compile('\d*\,*\d+g')
p2 = re.compile('\d*\,*\d+')
p3 = re.compile('[^\s\dg]+')
p4 = re.compile('[^\s]+')
## url을 통한 html 가져오기 ##
driver.get('http://www.mcfood.net/shop/shopbrand.html?xcode=022&type=X')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []
## 전체 메뉴 이미지와 베스트 메뉴 이미지가 있어 이를 구분하기위한 class 속성값 item_box로 접근
base = 'http://www.mcfood.net'
tt = soup.findAll('ul', {'class': 'item_box'})
for i in range(len(tt)):
    xx = tt[i].findAll('li', {'class': 'pname'})[1].text  # 중량 정보가 들어있는 텍스트
    if len(p1.findall(xx)) > 0:
        weight.append(int(p1.findall(xx)[0].replace(' ', '').replace(',', '').replace('g', '')))
    else:
        weight.append(None)

    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/mongchon/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    urllib.request.urlretrieve('http://www.mcfood.net' + tt[i].find('img')['src'], img_path)

    # 음식 가격#
    yy = tt[i].findAll('span', {'class': 'price'})
    price.append(int(p2.findall(yy[0].text)[0].replace(',', '')))

    # 음식 이름#
    zz = tt[i].findAll('li', {'class': 'pname'})[1].text
    name.append(p3.findall(zz)[0])

    url = base + tt[i].a['href']
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ww = soup.select('tr > td > span')[8].text
    material.append(''.join(p4.findall(ww)))

food_dict_list = []
for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'mongchon'
    temp['online_market_address'] = 'http://www.mcfood.net'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = weight[i]
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = None
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)


####################################################################################################################

### 집밥에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p1 = re.compile('[\d\,]*\d+')
p2 = re.compile('[\d\,]*\d+g')
# p3 = re.compile('[^\s\dg]+')
# p4 = re.compile('[^\s]+')
## url을 통한 html 가져오기 ##
driver.get('http://zipbab.com/product/list.html?cate_no=25')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []  # 이미지 저장 경로

bb = soup.findAll('li', {'class': 'item xans-record-'})
base = 'https://zipbab.com'
for i in range(len(bb)):
    name.append(bb[i].findAll('img')[1]['alt'])
    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/zipbab/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    urllib.request.urlretrieve('https:' + bb[i].findAll('img')[1]['src'], img_path)

    driver.get(base + bb[i].a['href'])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tt = soup
    price.append(int(p1.findall(tt.select('span > strong')[0].text)[0].replace(',', '')))
    if len(p2.findall(tt.tbody.findAll('tr')[5].td.text)) > 0:
        weight.append(int(p2.findall(tt.tbody.findAll('tr')[5].td.text)[0].replace('g', '')))
    else:
        weight.append(None)

    if tt.tbody.findAll('tr')[6].th.text == '재료':
        material.append(tt.tbody.findAll('tr')[6].td.text)
    else:
        material.append(None)

food_dict_list = []
for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'zipbab'
    temp['online_market_address'] = 'http://www.zipbab.com'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = weight[i]
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = None
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)

####################################################################################################################

# 비움반찬에서 음식정보 가져오는 크롤러

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p1 = re.compile('[\d\,]*\d+')
p2 = re.compile('\(.*?\)')
p3 = re.compile('\'.*?\'')
# p4 = re.compile('[^\s]+')
## url을 통한 html 가져오기 ##
driver.get('https://shop.biumfood.com/single.php?category=2')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []  # 이미지 저장 경로

bb = soup.findAll('div', {'class': 'itemBox'})
base = 'https://shop.biumfood.com'
for i in range(len(bb)):
    name.append(bb[i].h5.text)
    price.append(int(p1.findall(bb[i].p.find('span', {'class': 'price'}).text)[0].replace(',', '')))
    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/bium/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    # xx는 이미지 url을 담는 변수
    # if len(p2.findall(bb[i].findAll('div')[3]['style'])) >0:
    if bb[i].findAll('div')[3].has_attr('style') and len(p2.findall(bb[i].findAll('div')[3]['style'])) > 0:
        xx = p2.findall(bb[i].findAll('div')[3]['style'])[0].replace('(', '').replace(')', '').replace("'", '')
        driver.get(base + '/' + p3.findall(bb[i].findAll('div')[3]['onclick'])[0].replace("'", ''))
    else:
        if bb[i].findAll('div')[4]['style'] == 'cursor: pointer':
            xx = p2.findall(bb[i].findAll('div')[5]['style'])[0].replace('(', '').replace(')', '').replace("'", '')
            driver.get(base + '/' + p3.findall(bb[i].findAll('div')[5]['onclick'])[0].replace("'", ''))
        else:
            xx = p2.findall(bb[i].findAll('div')[4]['style'])[0].replace('(', '').replace(')', '').replace("'", '')
            driver.get(base + '/' + p3.findall(bb[i].findAll('div')[4]['onclick'])[0].replace("'", ''))

    urllib.request.urlretrieve(base + xx, img_path)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    ss = str(soup.find('div', {'class': 'pure-u-1-1 pure-u-md-1-2'})).split('</strong><br/>')[1]
    p4 = re.compile('[^\sdiv\/\<\>]+')
    material.append(p4.findall(ss)[0])

food_dict_list = []
for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'bium'
    temp['online_market_address'] = 'https://shop.biumfood.com'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = None
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = None
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)

####################################################################################################################

### 진가네반찬에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p1 = re.compile('[\d\,\.]*\d+k*g')  ## {}안에 있는 문자들 모두 가져오기
p2 = re.compile('[\d\,]*\d+')
## 음식에 대한 상세정보 페이지로 이동하기 위해 goods_no을 알아내는 코드
## url을 통한 html 가져오기 ##
driver.get('http://jinganebanchan.com/product/list_all.html?cate_no=84')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

total_page = len([x for x in soup.select('ol > li > a') if x.has_attr('class')])  # 페이지의 개수
base = 'http://jinganebanchan.com/product/list_all.html?cate_no=84'
page = 1
food_dict_list = []
while (page <= total_page):
    name = []  # 음식이름
    price = []  # 가격
    nutrient = []  # 영양소(아직 없음)
    material = []  # 재료
    weight = []  # 중량
    image_path = []  # 이미지 패스
    driver.get(base + '&page=' + str(page))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    bb = soup.findAll('div', {'class': 'item-body'})
    cc = soup.findAll('div', {'class': 'item-head'})
    for i in range(len(bb)):
        xx = bb[i].a.span.text
        if len(p1.findall(xx)) > 0:
            if 'k' in p1.findall(xx)[0]:
                weight.append(int(float(p1.findall(xx)[0].replace('kg', '')) * 1000))
            else:
                weight.append(int(p1.findall(xx)[0].replace('g', '')))
        else:
            weight.append(None)

        if len(p1.findall(xx)) > 0:
            name.append(xx.replace(p1.findall(xx)[0], '').replace(' ', ''))
        else:
            name.append(xx)

        yy = bb[0].div.findAll('li')[1].text
        price.append(int(p2.findall(yy)[0].replace(',', '')))

        img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/jingane/img_{0}_{1}.jpg'.format(page, i)
        image_path.append(img_path)
        urllib.request.urlretrieve('http:' + cc[i].img['src'], img_path)

        driver.get(base1 + bb[i].a['href'])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if len(soup.find('div', {'class': 'gosi-table'}).findAll('td')) > 0:
            material.append(soup.find('div', {'class': 'gosi-table'}).findAll('td')[7].text)
        else:
            material.append(None)

    for i in range(len(name)):
        temp = dict()
        temp['online_market_name'] = 'jingane'
        temp['online_market_address'] = 'http://jinganebanchan.com'
        temp['product_categorie'] = None
        temp['product_price'] = price[i]
        temp['product_weight'] = weight[i]
        temp['product_name'] = name[i]
        temp['product_raw_materials'] = material[i]
        temp['product_raw_content'] = None
        temp['product_image_path'] = image_path[i]
        temp['product_keyword'] = None
        temp['product_effect'] = None
        temp['product_kcal'] = None
        temp['product_carbon'] = None
        temp['product_protein'] = None
        temp['product_fat'] = None
        temp['product_sugar'] = None
        temp['product_na'] = None
        temp['product_chol'] = None
        temp['product_saturated_fat'] = None
        temp['product_trans_fat'] = None
        temp['update_date'] = None
        temp['product_group'] = None
        temp['product_type1'] = None
        temp['product_type2'] = None
        temp['product_type3'] = None
        food_dict_list.append(temp)
    page += 1

####################################################################################################################

### 반찬가게에서 음식정보 가져오는 크롤러 ###

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import json
import urllib
import os


## 함수 정의

def url_with_parameter(base, params):
    ## get방식의 파라미터를 이용하여 url을 완성시키는 함수
    ## check type!!
    if type(base) != str:
        raise TypeError('1st argument must be string.')
    if type(params) != dict:
        raise TypeError('2nd argument must be dictionary')

    base_url = base + '?'
    for k, v in params.items():
        if type(k) == str and type(v) == str:
            base_url += k + '=' + v + '&'
        else:
            raise TypeError('Key and value of dictionary are both string type')

    url = base_url[:len(base_url) - 1]  ## delete last '&'
    return url


## 사전 세팅 ##
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/Users/User/chromedriver_win32/chromedriver.exe', chrome_options=options)
driver.implicitly_wait(3)

## 정규표현식
p1 = re.compile('\d*\,*\d+')
p2 = re.compile('[\d\,\.]*\d+k*g')  ## {}안에 있는 문자들 모두 가져오기
# p2 = re.compile('[\d\,]*\d+')
## 음식에 대한 상세정보 페이지로 이동하기 위해 goods_no을 알아내는 코드
## url을 통한 html 가져오기 ##
driver.get('http://www.banchangage.com/goods/goods_list.php?cateCd=005')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
bb = soup.findAll('div', {'class': 'space'})

name = []  # 음식이름
price = []  # 가격
nutrient = []  # 영양소(아직 없음)
material = []  # 재료
weight = []  # 중량
image_path = []  # 이미지 패스

base = 'http://www.banchangage.com'
for i in range(len(bb)):
    name.append(bb[i].img['alt'])

    xx = bb[i].find('span', {'class': 'cost'}).text
    price.append(int(p1.findall(xx)[0].replace(',', '')))

    img_path = 'C:/workspace/1thefull_menu_recommend/templates/pic/bcgage/img_{0}.jpg'.format(i)
    image_path.append(img_path)
    try:
        urllib.request.urlretrieve(base + bb[i].button['data-goods-image-src'], img_path)

    except:
        try:
            r = requests.get(base + bb[i].button['data-goods-image-src'])
            if r.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(r.content)
                f.close
        except TypeError:
            r = requests.get(base + bb[i].img['data-original'])
            if r.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(r.content)
                f.close

    driver.get('http://www.banchangage.com' + bb[i].a['href'].replace('..', ''))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    xx = soup.findAll('tbody')[2]
    material.append(xx.findAll('td')[1].text)

for i in range(len(name)):
    temp = dict()
    temp['online_market_name'] = 'bcgage'
    temp['online_market_address'] = 'http://www.banchangage.com'
    temp['product_categorie'] = None
    temp['product_price'] = price[i]
    temp['product_weight'] = None
    temp['product_name'] = name[i]
    temp['product_raw_materials'] = material[i]
    temp['product_raw_content'] = None
    temp['product_image_path'] = image_path[i]
    temp['product_keyword'] = None
    temp['product_effect'] = None
    temp['product_kcal'] = None
    temp['product_carbon'] = None
    temp['product_protein'] = None
    temp['product_fat'] = None
    temp['product_sugar'] = None
    temp['product_na'] = None
    temp['product_chol'] = None
    temp['product_saturated_fat'] = None
    temp['product_trans_fat'] = None
    temp['update_date'] = None
    temp['product_group'] = None
    temp['product_type1'] = None
    temp['product_type2'] = None
    temp['product_type3'] = None
    food_dict_list.append(temp)


####################################################################################################################