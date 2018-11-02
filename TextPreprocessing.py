from collections import Counter

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

def number_to_kor(n):
    units = [''] + list('십백천')
    nums = '일이삼사오육칠팔구'
    result = []
    i = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r > 0:
            result.append(nums[r-1] + units[i])
        i += 1
    return ''.join(result[::-1])

def number_to_kor_exp(n):
    """1억미만의 숫자를 읽는 함수"""
    a, b = [number_to_kor(x) for x in divmod(n, 10000)]
    if a:
        return a + "만" +  b
    return b

def kor_to_number(m):
    ko_number = {'일':1,
              '이':2,
              '삼':3,
              '사':4,
              '오':5,
              '육':6,
              '칠':7,
              '팔':8,
              '구':9}
    ko_decimal1 = {'십':10,
                  '백':100,
                  '천':1000
                 }
    ko_decimal2 = {'만':10000,
                  '억':10000*10000,
                  '조':10000*10000*10000
                 }

    if len(set(list(m)).intersection(list(ko_decimal1.keys()))) == 0:
        try:
            if len(m) == 1:
                try:
                    return ko_number[m]
                except KeyError:
                    print('천단위가 넘거나 정확한 숫자가 아닙니다.')
            else:
                raise ValueError('천단위가 넘거나 정확한 숫자가 아닙니다.')
        except ValueError as ex:
            print(ex)
    else:
        value = 0
        decimal = list(set(list(m)).intersection(ko_decimal1))
        if '천' in decimal:
            try:
                index = [i for i,v in enumerate(list(m)) if v == '천']
                if index[0]-1 >=0:
                    unit1000 = ko_number[list(m)[index[0]-1]]
                else:
                    unit1000 = 1
            except:
                unit1000 = 1

            value += unit1000*1000
        if '백' in decimal:
            try:
                index = [i for i,v in enumerate(list(m)) if v == '백']
                if index[0]-1 >=0:
                    unit100 = ko_number[list(m)[index[0]-1]]
                else:
                    unit100 = 1
            except:
                unit100 = 1
            value += unit100*100

        if '십' in decimal:
            try:
                index = [i for i,v in enumerate(list(m)) if v == '십']
                if index[0]-1 >=0:
                    unit10 = ko_number[list(m)[index[0]-1]]
                else:
                    unit10 = 1
            except:
                unit10 = 1
            try:
                index = [i for i,v in enumerate(list(m)) if v == '십']
                unit1 = ko_number[list(m)[index[0]+1]]
            except:
                unit1 = 0
            value += unit10*10
            value += unit1
        return value

def jaro_distance(s1, s2, p=0.1):
    m = len(set(list(s1)).intersection(list(s2)))
    if m == 0:
        return 0
    else:
        if len(s1) == len(s2):
            c = [x for x in s1 if x in set(s2)]
            t = 0
            for i in c:
                if s1.index(i) != s2.index(i):
                    t += 1
        else:
            t = 0
        dj = (m / len(s1) + m / len(s2) + 1 - t / m) / 3
        l = max(map(len, find_common_word(s1, s2, split_space=False, drop_onelength=False)))
        if p > 0.25:
            raise ValueError("p는 0.25를 넘을 수 없습니다.")
        dw = dj + l * p * (1 - dj)
        return dw