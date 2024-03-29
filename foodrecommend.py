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

def recommend_food(gender, age, preg, kinds, df1, df2):
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
