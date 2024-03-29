# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import urllib
import pdb
from dbmanager_singleton import db_manager



class market_fooding:
    market_name='fooding'
    market_address = 'http://www.fooding.io/'
    name = []  # 음식이름
    price = []  # 가격
    nutrient = []  # 영양소(아직 없음)
    material = []  # 재료
    weight = []  # 중량

    
    def __init__(self):
        self.dbmanager = db_manager()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=self.options)
        self.driver.implicitly_wait(3)
        self.driver.get('http://www.fooding.io/after-filter?week=&time=&headcount=&type=1&search_content=')

        with urllib.request.urlopen('http://api.fooding.io/search?price=&week=&time=&headcount=&filter_list=&type=1&search_content=') as url:
            self.data = json.loads(url.read().decode())

        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html,'html.parser')
        self.p = re.compile('^(\d+[a-z])')
        self.p1 = re.compile('(\w+\(?\w+\)?)')
        self.p2 = re.compile('(\d+)')
        self.selected_data = self.dbmanager.select_market_product("fooding")
        self.column_dict = self.selected_data[0].keys()
        pdb.set_trace()


    def get_data(self):
        for i in range(len(self.data['product_list'])):
            self.name.append(self.data['product_list'][i]['item_name'])
            if self.data['product_list'][i]['sale_price'] == None:
                self.price.append(self.data['product_list'][i]['price'])
            else:
                self.price.append(self.data['product_list'][i]['sale_price'])

        for i in range(len(self.data['product_list'])):
            while (1):
                self.food_id = self.data['product_list'][i]['item_id']
                self.driver.get('http://www.fooding.io/detail/' + str(self.food_id) + '/1')
                self.html = self.driver.page_source
                self.soup = BeautifulSoup(self.html, 'html.parser')
                self.bb = self.soup.findAll('span', {'class': 'value'})[2].get_text()
                self.cc = self.soup.findAll('span', {'class': 'value'})[3].get_text()
                if len(self.p1.findall(self.cc)) == 0:
                    pass
                else:
                    self.weight.append(int(self.p2.findall(self.cc)[0]))
                    self.material.append(self.p1.findall(self.bb))
                    break

            ## 만약 재료와 원산지를 따로 구분하고 싶다면
        self.aa = self.material[0]
        self.origin = [x.split('(')[1].replace(')', '') for x in self.aa]  ## 괄호 안에 있는 단어 추출
        self.material_only = [x.split('(')[0] for x in self.aa]  ## 괄호 왼쪽에 있는 단어 추출

    def print(self):
        print(self.name)
        print(self.price)
        print(self.nutrient)
        print(self.material)
        print(self.weight)
        print(self.origin)
        print(self.material_only)

    def compare_db_data(self):
        print('test')
