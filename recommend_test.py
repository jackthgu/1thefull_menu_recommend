# -*- coding: utf-8 -*- 

import json
import pandas as pd
import itertools as it
import numpy as np
import requests
import re
import time
import os
from urllib import parse
from collections import OrderedDict, Counter
from flask import Flask, request



filename1 = 'data/cooknutrienttable.csv'
filename2 = 'data/recommendednutrienttable.csv'
filepath1 = os.path.join(os.path.dirname(__file__), filename1)
filepath2 = os.path.join(os.path.dirname(__file__), filename2)
df1 = pd.read_csv(filepath1, engine='python')
df2 = pd.read_csv(filepath2, engine='python')

def extract_nutrient(df, food):
    if food.isalnum() == False:
        food = ''.join(e for e in food if e.isalnum())

    b = list(df[df.columns[2]].map(lambda x : x.replace(' ','')))
    if food in b:
        temp = [i for i,v in enumerate(b) if v == food]
        if len(temp) == 1:
            index = temp[0]
            return df[df.columns[2]].iloc[index], df.loc[:,df.columns[3]:df.columns[12]].iloc[index]
        else:
            index = temp
            return food, df.loc[:,df.columns[3]:df.columns[12]].iloc[index].mean()
    else:
        word_len = []
        for i in range(len(df)):
            if len(find_common_word(food,df[df.columns[2]].iloc[i],False,True)) >= 1:
                a = len(find_common_word(food,df[df.columns[2]].iloc[i],False,True)[0])
                word_len.append(a/len(df[df.columns[2]].iloc[i].replace(' ','')))
            else:
                word_len.append(0)
        index = [i for i,v in enumerate(word_len) if v > 0]
        temp = list(df[df.columns[2]].iloc[index].map(lambda x : x.replace(' ','')))
        #p = re.compile(food)
        #res = []
        #for i in temp:
            #m = p.match(i)
            #if m:
                #res.append(i)
        res = []
        for i in temp:
            if food in i:
                res.append(i)

        if len(res) >1 :
            temp = [i for i,v in enumerate(b) if v == res[0]]
            index = temp
            return food, df.loc[:,df.columns[3]:df.columns[12]].iloc[index].mean()
        elif len(res) == 1:
            temp = [i for i,v in enumerate(b) if v == res[0]]
            index = temp[0]
            return df[df.columns[2]].iloc[index], df.loc[:,df.columns[3]:df.columns[12]].iloc[index]
        else:
            return 0

def recommend_food_temp(gender, age, preg, kinds, df1, df2):
    # gender = 성별, age = 연령대, preg = 임신여부, df1 = 음식 영양소 데이터, df2 = 권장영양소 섭취량 데이터
    b = df2.loc[(df2['gender']==gender) & (df2['age']==age)]

    # 일단 반찬같은거는 무시한다고 가정
    ## 일단 밥류로 한정하여 권장칼로리에 가장가까운 아침점심저녁 추천
    ## 알러지 문제, 반찬추가, 데이터 정제
    temp = df1[df1['식품군']==kinds]
    index_range = list(range(len(temp)))
    index_combination = [list(x) for x in it.combinations(index_range,3)]

    temp_index = []
    for i in index_combination:
        temp_list = []
        for j in range(5,13):
            temp_list.append(temp[temp.columns[j]].iloc[i])
        res = list(map(sum, temp_list))
        if preg == 0:
            if res[0] <= float(b['carbo2']) and \
            res[1] <= float(b['protein2']) and \
            res[2] <= float(b['fat2']) and \
            res[3] <= float(b['sugar2']) and \
            res[4] <= float(b['na']) and \
            res[5] <= float(b['chol']) and \
            res[6] <= float(b['saturated fat']) and \
            res[7] <= float(b['trans fat']):
                temp_index.append(i)
        elif preg == 1:
            if res[0] <= float(b['carbo2']) and \
            res[1] <= float(b['protein2']) and \
            res[2] <= float(b['fat2']) and \
            res[3] <= float(b['sugar2']) and \
            res[4] <= 1500 and \
            res[5] <= float(b['chol']) and \
            res[6] <= float(b['saturated fat']) and \
            res[7] <= float(b['trans fat']):
                temp_index.append(i)
        elif preg == 2:
            if res[0] <= float(b['carbo2']) and \
            res[1] <= float(b['protein2']) + 13.5 and \
            res[2] <= float(b['fat2']) and \
            res[3] <= float(b['sugar2']) and \
            res[4] <= 1500 and \
            res[5] <= float(b['chol']) and \
            res[6] <= float(b['saturated fat']) and \
            res[7] <= float(b['trans fat']):
                temp_index.append(i)
        else:
            if res[0] <= float(b['carbo2']) and \
            res[1] <= float(b['protein2']) + 27.5 and \
            res[2] <= float(b['fat2']) and \
            res[3] <= float(b['sugar2']) and \
            res[4] <= 1500 and \
            res[5] <= float(b['chol']) and \
            res[6] <= float(b['saturated fat']) and \
            res[7] <= float(b['trans fat']):
                temp_index.append(i)

    kcal_sum = []
    for i in range(len(temp_index)):
        kcal_sum.append(sum(temp[temp.columns[4]].iloc[temp_index[i]]))

    if preg == 0:
        recommend = list(map(abs,list(map(lambda x:x-int(b['recommended cal']),kcal_sum))))
    elif preg == 1:
        recommend = list(map(abs,list(map(lambda x:x-int(b['recommended cal']),kcal_sum))))
    elif preg == 2:
        recommend = list(map(abs,list(map(lambda x:x-(int(b['recommended cal'])+340),kcal_sum))))
    else:
        recommend = list(map(abs,list(map(lambda x:x-(int(b['recommended cal'])+450),kcal_sum))))

    min_index = [i for i,v in enumerate(recommend) if v == min(recommend)]
    if len(min_index) > 0:
        a = temp.iloc[temp_index[min_index[0]]]
    else:
        sys.exit('최적 식단을 찾을수 없습니다.')

    bb = list(a.sort_values(a.columns[4])[a.columns[2]])
    bb[0], bb[1], bb[2] = bb[1], bb[2], bb[0]
    food_name = bb
    res_list = []
    for j in range(4,13):
        res_list.append(temp.iloc[temp_index[min_index[0]]][temp.columns[j]])

    res_list = list(map(sum,res_list))
    return food_name, res_list

def scrap_weather():
    response = requests.get('https://pythondojang.bitbucket.io/weather/observation/currentweather.html')
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', { 'class': 'table_develop3' })    # <table class="table_develop3">을 찾음
    data = []                            # 데이터를 저장할 리스트 생성
    for tr in table.findAll('tr'):      # 모든 <tr> 태그를 찾아서 반복(각 지점의 데이터를 가져옴)
        tds = tr.find_all('td')    # 모든 <td> 태그를 찾아서 리스트로 만듦
                                         # (각 날씨 값을 리스트로 만듦)
        for td in tds:                   # <td> 태그 리스트 반복(각 날씨 값을 가져옴)
            if td.find('a'):             # <td> 안에 <a> 태그가 있으면(지점인지 확인)
                point = td.find('a').text    # <a> 태그 안에서 지점을 가져옴
                temperature = tds[5].text    # <td> 태그 리스트의 여섯 번째(인덱스 5)에서 기온을 가져옴
                humidity = tds[9].text       # <td> 태그 리스트의 열 번째(인덱스 9)에서 습도를 가져옴
                data.append([point, temperature, humidity])    # data 리스트에 지점, 기온, 습도를 추가
    return data

def cal_discomfortindex(temperature,humidity):
    res = 9*temperature/5 - 0.55*(1-humidity/100)*(9*temperature/5-26)+32
    if res >= 80:
        level = 4
    elif res < 80 and res >= 75:
        level = 3
    elif res < 75 and res >= 68:
        level = 2
    else:
        level = 1
    return res, level

def recommend_food(gender, age, preg, kinds, df1, df2, hbp='', diabetes='', diet=''):
    b = df2.loc[(df2['gender'] == gender) & (df2['age'] == age)]

    # 일단 반찬같은거는 무시한다고 가정
    ## 일단 밥류로 한정하여 권장칼로리에 가장가까운 아침점심저녁 추천
    ## 알러지 문제, 반찬추가, 데이터 정제
    temp = df1.loc[(df1['type2'] == kinds) & (df1['type1'] == '메인')]
    if hbp == 1:
        temp = temp[temp['hbp'] == 1]
    if diabetes == 1:
        temp = temp[temp['diabetes'] == 1]
    if diet == 1:
        temp = temp[temp['diet'] == 1]

    index_range = list(range(len(temp)))

    temp_index = []
    for i in index_range:
        temp_list = []
        for j in range(8, 16):
            temp_list.append(temp[temp.columns[j]].iloc[i])
        res = temp_list
        if preg == 0:
            if res[0] <= float(b['carbo2'] / 3) and \
                    res[1] <= float(b['protein2'] / 3) and \
                    res[2] <= float(b['fat2'] / 3) and \
                    res[3] <= float(b['sugar2'] / 3) and \
                    res[4] <= float(b['na'] / 3) and \
                    res[5] <= float(b['chol'] / 3) and \
                    res[6] <= float(b['saturated fat'] / 3) and \
                    res[7] <= float(b['trans fat'] / 3):
                temp_index.append(i)
        elif preg == 1:
            if res[0] <= float(b['carbo2'] / 3) and \
                    res[1] <= float(b['protein2'] / 3) and \
                    res[2] <= float(b['fat2'] / 3) and \
                    res[3] <= float(b['sugar2'] / 3) and \
                    res[4] <= 500 and \
                    res[5] <= float(b['chol'] / 3) and \
                    res[6] <= float(b['saturated fat'] / 3) and \
                    res[7] <= float(b['trans fat'] / 3):
                temp_index.append(i)
        elif preg == 2:
            if res[0] <= float(b['carbo2'] / 3) and \
                    res[1] <= (float(b['protein2']) + 13.5) / 3 and \
                    res[2] <= float(b['fat2'] / 3) and \
                    res[3] <= float(b['sugar2'] / 3) and \
                    res[4] <= 500 and \
                    res[5] <= float(b['chol'] / 3) and \
                    res[6] <= float(b['saturated fat'] / 3) and \
                    res[7] <= float(b['trans fat'] / 3):
                temp_index.append(i)
        else:
            if res[0] <= float(b['carbo2'] / 3) and \
                    res[1] <= (float(b['protein2']) + 27.5) / 3 and \
                    res[2] <= float(b['fat2'] / 3) and \
                    res[3] <= float(b['sugar2'] / 3) and \
                    res[4] <= 500 and \
                    res[5] <= float(b['chol'] / 3) and \
                    res[6] <= float(b['saturated fat'] / 3) and \
                    res[7] <= float(b['trans fat'] / 3):
                temp_index.append(i)

    a = list(range(len(temp_index)))
    index = random.choices(a, k=1)[0]
    bb = temp_index[index]
    food_name = temp['fdname'].iloc[bb]

    nut_info = []
    for i in range(6, 16):
        nut_info.append(float(temp[temp['fdname'] == food_name][temp.columns[i]]))
    return food_name, nut_info


def find_common_word(b, c, split_space=True, drop_onelength=True):
    # 두 텍스트의 공통 단어를 찾는 함수

    # 예외 처리
    if type(b) != str:
        raise ValueError('첫 번째 입력값은 문자 혹은 문장이어야 합니다.')
    if type(c) != str:
        raise ValueError('두 번째 입력값은 문자 혹은 문장이어야 합니다.')
    if split_space == False:
        b = b.replace(' ', '')
        c = c.replace(' ', '')
        common_word = []

        def all_ngrams(text):
            ngrams = (text[i:i + n] for n in range(1, len(text) + 1)
                      for i in range(len(text) - n + 1))
            return Counter(ngrams)

        def intersection(string1, string2):
            count_1 = all_ngrams(string1)
            count_2 = all_ngrams(string2)
            return count_1 & count_2  # intersection:  min(c[x], d[x])

        while (1):
            aa = dict(intersection(b, c))
            if len(aa) == 0:
                break
            else:
                len_list = [len(x) for x in list(aa.keys())]
                res = {k: v for k, v in aa.items() if len(k) == max(len_list)}

                for k, v in res.items():
                    common_word.append(k)
                    b = b.replace(k, '')
                    c = c.replace(k, '')
        if drop_onelength == True:
            common_word = [x for x in common_word if len(x) != 1]
        return common_word
    else:
        res1 = [x for x in b.split(' ') if x != '']
        res2 = [x for x in c.split(' ') if x != '']
        common_word = set(res1).intersection(res2)
        if drop_onelength == True:
            common_word = [x for x in common_word if len(x) != 1]
        return common_word

def over_nutrient(gender, age, preg, lunchlist, df1, df2):
    # gender = 성별, age = 연령, preg = 임신여부, lunchlist = 점심리스트, df2 = 권장 섭취 영양소 데이터
    nutrientlist = []
    noinfoindex = []
    for i in range(len(lunchlist)):
        if extract_nutrient(df1,lunchlist[i]) != 0:
            nutrientlist.append(extract_nutrient(df1,lunchlist[i]))
        else:
            noinfoindex.append(i)

    if len(noinfoindex) >=1:
        noinfolist = [v for i,v in enumerate(lunchlist) if i in noinfoindex]
    else:
        noinfolist = ''
        pass

    if len(nutrientlist) >=1:
        avernutrient = sum(nutrientlist[j][1] for j in range(len(nutrientlist)))/len(nutrientlist)
        avernutrient = avernutrient[1:]
    #avernutrient = [0,0,0,0,0,0,0,0,0]
        foodname = [nutrientlist[j][0] for j in range(len(nutrientlist))]
    else:
        raise ValueError('영양소 정보를 찾을 수 없습니다.')

    b = df2.loc[(df2['gender']==gender) & (df2['age']==age)]
    if preg == 0:
        pass
    elif preg == 1:
        b['na'] = 1500
    elif preg == 2:
        b['recommended cal'] += 340
        b['protein2'] += 13.5
        b['na'] = 1500
    else:
        b['recommended cal'] += 450
        b['protein2'] += 27.5
        b['na'] = 1500

    nutrientname = ['열량', '탄수화물', '단백질', '지방', '당', '나트륨', '콜레스테롤', '포화지방', '트랜스지방']
    comparison = [int(b['recommended cal']/3), float(b['carbo2']/3), float(b['protein2']/3), float(b['fat2']/3),\
                 float(b['sugar2']/3), float(b['na']/3), float(b['chol']/3), float(b['saturated fat']/3), float(b['trans fat']/3)]

    #for i in range(len(avernutrient)):
    a=[i if v > comparison[i]  else -1 for i, v in enumerate(list(avernutrient))]
    index = [i for i in a if i>=0]
    overnutrient = []
    for i in index:
        overnutrient.append(nutrientname[i])

    if len(overnutrient) >=1:
        return overnutrient, noinfolist
    else:
        return 'normal', noinfolist

app = Flask(__name__)

@app.route('/foodrecommend/service1', endpoint='service1')
def service1():
    try:
        # 데이터 포맷 #
        group_data = OrderedDict()

        # 하루 동안 먹은 음식 리스트 #
        fdlist = request.args.get('fdlist', type=str)
        fdlist = parse.unquote(fdlist)
        # 에외 처리

        if len(fdlist) == 0:
            raise ValueError('음식을 적어 주세요~')

        fdlist = [x.replace(' ','') for x in fdlist.split(',')]

        a = []
        b = ''
        c = []
        for i in fdlist:
            if extract_nutrient(df1, i) != 0:
                a.append(extract_nutrient(df1, i)[1])
                c.append(extract_nutrient(df1, i)[0])
            else:
                b = b + i + ', '

        if len(b) > 2:
            exmg = b[:-2] + '에 대한 음식정보는 없습니다.'
        else:
            exmg = ''

        if len(a) != 0:
            bb = sum(a)
            b1 = ['1회제공량', '열량', '탄수화물', '단백질', '지방', '당', '나트륨', '콜레스테롤', '포화지방', '트랜스지방']
            cc = bb.to_dict()
            aa = [float(format(x, '.2f')) for x in cc.values()]
            result = dict(zip(b1, aa))
            result.pop('1회제공량')
            foodname = c
        else:
            result = ''
            foodname = ''

        group_data['status'] = 'ok'
        group_data['type'] = 1
        group_data['foodname'] = foodname
        group_data['result'] = result
        group_data['message'] = exmg
        #group_data['elapsed_time'] = elapsed_time
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')

        return response

    except ValueError as ex:
        group_data = OrderedDict()
        group_data['status'] = 'error'
        group_data['error_message'] = str(ex)
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')
        return response

@app.route('/foodrecommend/service2', endpoint='service2')
def service2():
    try:
        # 데이터 포맷 #
        group_data = OrderedDict()

        # 하루 동안 먹은 음식 리스트 #
        gender = request.args.get('gender', type=int)
        age = request.args.get('age', type=int)
        preg = request.args.get('preg', type=int)
        fdlist = request.args.get('fdlist', type=str)
        fdlist = parse.unquote(fdlist)
        # 에외 처리
        if type(gender) != int:
            raise ValueError('성별을 선택하세요')
        if type(age) != int:
            raise ValueError('연령대를 선택세요')
        if gender == 0 and type(preg) != int:
            raise ValueError('임신 여부를 선택하세요')
        if len(fdlist) == 0:
            raise ValueError('음식을 적어 주세요~')

        fdlist = [x.replace(' ','') for x in fdlist.split(',')]
        a = []
        b = ''
        c = []
        for i in fdlist:
            if extract_nutrient(df1, i) != 0:
                a.append(extract_nutrient(df1, i)[1])
                c.append(extract_nutrient(df1, i)[0])
            else:
                b = b + i + ', '

        if len(b) > 2:
            exmg = b[:-2] + '에 대한 음식정보는 없습니다.'
        else:
            exmg = ''

        if len(a) != 0:
            bb = sum(a)
            b1 = ['1회제공량', '열량', '탄수화물', '단백질', '지방', '당', '나트륨', '콜레스테롤', '포화지방', '트랜스지방']
            cc = bb.to_dict()
            aa = [float(format(x, '.2f')) for x in cc.values()]
            result = dict(zip(b1, aa))
            result.pop('1회제공량')
            foodname = c
        else:
            result = ''
            foodname = ''

        # 권장 영양소 정보 #
        a = df2.loc[(df2['gender'] == gender) & (df2['age'] == age)]
        if preg == 0:
            res = a
        elif preg == 1:
            a['na'] = 1500
        elif preg == 2:
            a['recommended cal'] = a['recommended cal'] + 340
            a['na'] = 1500
            a['protein2'] = a['protein2'] + 13.5
        elif preg == 3:
            a['recommended cal'] = a['recommended cal'] + 450
            a['na'] = 1500
            a['protein2'] = a['protein2'] + 27.5

        b = {'열량': int(a['recommended cal']), '탄수화물': float(a['carbo2']), '단백질': float(a['protein2']),
             '지방': float(a['fat2']), '당': float(a['sugar2']), '나트륨': float(a['na']), \
             '콜레스테롤': int(a['chol']), '포화지방': float(a['saturated fat']), '트랜스지방': float(a['trans fat'])}
        bb = [float(format(x, '.2f')) for x in b.values()]
        result2 = dict(zip(b.keys(), bb))
        over = []
        per = []
        if len(result) != 0:
            for k, v in result.items():
                if v >= result2[k]:
                    over.append(k)
                    x = float(format(100 * (v - result2[k]) / result2[k], '.2f'))
                    per.append(x)
            if len(over) > 0:
                subres = dict(zip(over, per))
            else:
                subres = {'': ''}
        else:
            subres = {'': ''}

        group_data['status'] = 'ok'
        group_data['type'] = 2
        group_data['result'] = result
        group_data['result2'] = result2
        group_data['result3'] = subres
        group_data['message'] = exmg
        #group_data['elapsed_time'] = elapsed_time
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')

        return response

    except ValueError as ex:
        group_data = OrderedDict()
        group_data['status'] = 'error'
        group_data['error_message'] = str(ex)
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')
        return response

@app.route('/foodrecommend/service3', endpoint='service3')
def service3():
    try:
        # 데이터 포맷 #
        group_data = OrderedDict()

        # 하루 동안 먹은 음식 리스트 #
        gender = request.args.get('gender', type=int)
        age = request.args.get('age', type=int)
        preg = request.args.get('preg', type=int)
        #kinds = request.args.get('kinds', type=str)
        #kinds = parse.unquote(kinds)
        kinds = '밥류'
        # 에외 처리
        if type(gender) != int:
            raise ValueError('성별을 선택하세요')
        if type(age) != int:
            raise ValueError('연령대를 선택세요')
        if gender == 0 and type(preg) != int:
            raise ValueError('임신 여부를 선택하세요')
        if len(kinds) == 0:
            raise ValueError('음식 종류를 선택하세요~')

        result = recommend_food(gender,age,preg,kinds,df1,df2)
        fdlist = result[0]
        a = []
        b = ''
        c = []
        for i in fdlist:
            if extract_nutrient(df1, i) != 0:
                a.append(extract_nutrient(df1, i)[1])
                c.append(extract_nutrient(df1, i)[0])
            else:
                b = b + i + ', '

        if len(b) > 2:
            exmg = b[:-2] + '에 대한 음식정보는 없습니다.'
        else:
            exmg = ''

        if len(a) != 0:
            bb = sum(a)
            b1 = ['1회제공량', '열량', '탄수화물', '단백질', '지방', '당', '나트륨', '콜레스테롤', '포화지방', '트랜스지방']
            cc = bb.to_dict()
            aa = [float(format(x, '.2f')) for x in cc.values()]
            temp = dict(zip(b1, aa))
            temp.pop('1회제공량')
            foodname = c
        else:
            result = ''
            foodname = ''

        group_data['status'] = 'ok'
        group_data['type'] = 3
        group_data['result'] = result[0]
        group_data['result1'] = temp
        #group_data['message'] = exmg
        #group_data['elapsed_time'] = elapsed_time
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')

        return response

    except ValueError as ex:
        group_data = OrderedDict()
        group_data['status'] = 'error'
        group_data['error_message'] = str(ex)
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')
        return response

@app.route('/foodrecommend/service4', endpoint='service4')
def service4():
    try:
        # 데이터 포맷 #
        group_data = OrderedDict()

        # 하루 동안 먹은 음식 리스트 #
        gender = request.args.get('gender', type=int)
        age = request.args.get('age', type=int)
        preg = request.args.get('preg', type=int)
        #kinds = request.args.get('kinds', type=str)
        #kinds = parse.unquote(kinds)
        kinds = '밥류'
        # 에외 처리
        if type(gender) != int:
            raise ValueError('성별을 선택하세요')
        if type(age) != int:
            raise ValueError('연령대를 선택세요')
        if gender == 0 and type(preg) != int:
            raise ValueError('임신 여부를 선택하세요')
        if len(kinds) == 0:
            raise ValueError('음식 종류를 선택하세요~')

        result = recommend_food(gender,age,preg,kinds,df1,df2)
        fdlist = result[0]
        a = []
        b = ''
        c = []
        for i in fdlist:
            if extract_nutrient(df1, i) != 0:
                a.append(extract_nutrient(df1, i)[1])
                c.append(extract_nutrient(df1, i)[0])
            else:
                b = b + i + ', '

        if len(b) > 2:
            exmg = b[:-2] + '에 대한 음식정보는 없습니다.'
        else:
            exmg = ''

        if len(a) != 0:
            bb = sum(a)
            b1 = ['1회제공량', '열량', '탄수화물', '단백질', '지방', '당', '나트륨', '콜레스테롤', '포화지방', '트랜스지방']
            cc = bb.to_dict()
            aa = [float(format(x, '.2f')) for x in cc.values()]
            temp = dict(zip(b1, aa))
            temp.pop('1회제공량')
            foodname = c
        else:
            result = ''
            foodname = ''

        group_data['status'] = 'ok'
        group_data['type'] = 3
        group_data['result'] = result[0]
        group_data['result1'] = temp
        #group_data['message'] = exmg
        #group_data['elapsed_time'] = elapsed_time
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')

        return response

    except ValueError as ex:
        group_data = OrderedDict()
        group_data['status'] = 'error'
        group_data['error_message'] = str(ex)
        response = json.dumps(group_data, ensure_ascii=False, indent='\t')
        return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4996)
