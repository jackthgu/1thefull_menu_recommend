from konlpy.tag import Kkma
from konlpy.utils import pprint
kkma = Kkma()

# pprint(kkma.sentences(u'네, 안녕하세요. 반갑습니다.'))

aaa = '안녕하세요'
aa = kkma.pos(aaa)

print(aa)