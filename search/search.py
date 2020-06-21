# 검색 엔진
import os
import re

import django
import numpy as np
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup

from .rq_class import *



### 데이터 처리 메소드
def findTag(lst, tag):
    return lst[lst.index(tag)+1]

# 모든 검색결과 파싱
def parseAll(req):
    result = []

    tmp = requests.get(req)
    soup = BeautifulSoup(tmp.content, 'html.parser')
    
    # 파싱할 페이지 수 카운트
    c_tmp = list(re.split('[<>]', str(soup.select('totalcount'))))
    try:
        page_count = int(findTag(c_tmp, 'totalcount'))
    except:
        page_count = 1
    
    if page_count < 10:
        page_count = 1
    else:
        page_count = (page_count // 10) + 1
    
    
    # 내용 파싱
    for i in range(1, page_count+1):
        req_tmp = req+'&{0}={1}'.format('pageNo', i)

        res_tmp = requests.get(req_tmp)
        soup = BeautifulSoup(res_tmp.content, 'html.parser')
        data = soup.find_all('item')

        if data:
            result.extend(data)
        else:
            break
    
    return result # 결과 리스트 반환

# 한 페이지만 파싱
def parseOne(req):
    result = []

    req = req + '&pageNo=1'
    tmp = requests.get(req)
    soup = BeautifulSoup(tmp.content, 'html.parser')
    data = soup.find_all('item')
    
    for elm in data:
        result.append(elm)

    return result


# 태그 낀 객체에서 검색결과 분해하기
def getInfos(tag_obj):
    # 태그 <> / 문자 등 제거
    tmp = re.split('[<>]', str(tag_obj))

    for elm in tmp:
        if '/' in elm or elm == 'item': 
            if 'http' in elm: continue
            else: tmp.remove(elm)
    while '' in tmp: tmp.remove('')
    while '[' in tmp: tmp.remove('[')
    while ']' in tmp: tmp.remove(']')
    while '\n' in tmp: tmp.remove('\n')

    # 요소 정리
    infos = {}
    
    try:
        for i in range(0, len(tmp), 2):
            infos[tmp[i]] = tmp[i+1]
        return infos # 딕셔너리 형태로 반환
    except:
        return 'num of contents is not an even number. check it out.'


# 중복 제거 후 반환(리스트, 리스트 원소=딕셔너리 일 때)
def checkInfos(lst, key):
    hash_space = set()
    new_lst = []
    for elm in lst:
        if hash(elm[key]) not in hash_space:
            hash_space.add(hash(elm[key]))
            new_lst.append(elm)
        else: continue
    return new_lst


# 지역코드값 대치
# 코드값 받아오면 한글 명칭으로 바꿔줌
def findGeo(df, dic):
    if not geo_file: return

    try:
        result = {'code1':'', 'code2':'',}

        val1 = int(dic['areacode'])
        val2 = int(dic['sigungucode'])

        row = df[ (df['city_code'] == val1) & (df['sigungu_code'] == val2) ]

        result['code1'] = row.iloc[0, 1]
        result['code2'] = row.iloc[0, 3]

        dic['areacode'] = result['code1']
        dic['sigungucode'] = result['code2']
    except:
        return
    

# 서비스코드값 대치
# 코드값 받아오면 한글 명칭으로 바꿔줌
def findSer(df, dic):
    if not ser_file: return

    try:
        result = {'code1':'', 'code2':'', 'code3':'',}
        val1 = dic['cat1']
        val2 = dic['cat2']
        val3 = dic['cat3']
        
        row = df[df['code3'] == str(val3)]

        result['code1'] = row.iloc[0, 1]
        result['code2'] = row.iloc[0, 3]
        result['code3'] = row.iloc[0, 5]

        dic['cat1'] = result['code1']
        dic['cat2'] = result['code2']
        dic['cat3'] = result['code3']
    except:
        return
    

### 데이터 처리 메소드 -끝-


### 검색 메소드

# 키워드로 검색
def searchByKeyword(word, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('keyword', word)
    return parseAll(req.makeReq(apiInfo.url, 'searchKeyword'))

# 무장애 정보 조회
def searchBF(id, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('contentId', id)
    tmp = parseAll(req.makeReq(apiInfo.url, 'detailWithTour'))
    result = getInfos(tmp)
    return result
    
# 상세 정보 조회
def searchDetails(contentId, typeId, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('contentId', contentId)

    # 이미지갤러리
    images = []
    tmp3 = parseAll(req.makeReq(apiInfo.url, 'detailImage'))
    for items in tmp3:
        images.append(getInfos(items))

    # 반복내용조회
    repetitive = []
    req.addPara('contentTypeId', typeId)
    tmp1 = parseAll(req.makeReq(apiInfo.url, 'detailInfo'))
    for items in tmp1:
        repetitive.append(getInfos(items))
    

    # 소개정보조회
    introduction = []
    tmp2 = parseAll(req.makeReq(apiInfo.url, 'detailIntro'))
    for items in tmp2:
        introduction.append(getInfos(items))

    infos = {'img':images, 'rep':repetitive, 'intro':introduction}


    return infos


# 인기장소 검색(n개, 사진 필수/무방 옵션)
def popularSites(site_num, pic_option, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('numOfRows', site_num)

    if pic_option:
        req.addPara('arrange', 'P')
    else:
        req.addPara('arrange', 'B')

    tmp = parseOne(req.makeReq(apiInfo.url, 'areaBasedList'))
    
    sites = []
    for elm in tmp:
        sites.append(getInfos(elm))

    return sites

# 0개의 장소 평가를 가지고 있는 초기 사용자에게 top8 장소 평가 제공
def initialSites(site_num, pic_option, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('numOfRows', site_num)

    rn_arrange = random.randint(0,3)
    rn_geocode = random.randint(1,39)

    if pic_option:
        req.addPara('arrange', 'P')
    else:
        req.addPara('arrange', 'B')

    tmp = parseOne(req.makeReq(apiInfo.url, 'areaBasedList'))
    
    results_list = []
    for elm in tmp:
        elm_tmp = getInfos(elm)
        dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid'),
        'firstimage':elm_tmp.get('firstimage')}
        results_list.append(dic_tmp)

    return results_list

# 무작위장소 검색(n개, 사진 필수/무방 옵션)
def randomSites(site_num, pic_option, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('numOfRows', site_num)

    rn_arrange = random.randint(0,3)
    rn_geocode = random.randint(1,39)

    if pic_option:
        if rn_arrange == 0:
            req.addPara('arrange', 'O')
        elif rn_arrange == 1:
            req.addPara('arrange', 'P')
        elif rn_arrange == 2:
            req.addPara('arrange', 'Q')
        elif rn_arrange == 3:
            req.addPara('arrange', 'R')
    else:
        if rn_arrange == 0:
            req.addPara('arrange', 'A')
        elif rn_arrange == 1:
            req.addPara('arrange', 'B')
        elif rn_arrange == 2:
            req.addPara('arrange', 'C')
        elif rn_arrange == 3:
            req.addPara('arrange', 'D')
    
    req.addPara('areaCode', rn_geocode)

    tmp = parseOne(req.makeReq(apiInfo.url, 'areaBasedList'))
    
    results_list = []
    for elm in tmp:
        elm_tmp = getInfos(elm)
        dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid'),
        'firstimage':elm_tmp.get('firstimage')}
        results_list.append(dic_tmp)

    return results_list

def simUserSites(words, site_num, pic_option, apiInfo):
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('numOfRows', site_num)

    if pic_option:
        req.addPara('arrange', 'P')
    else:
        req.addPara('arrange', 'B')

    sites = []
    for i in words :
        req.addPara('keyword', i)
        elm = parseOne(req.makeReq(apiInfo.url, 'searchKeyword'))[0]
        sites.append(getInfos(elm))
    
    return sites





### 검색 메소드 -끝-



### 데이터 처리용 변수

# tag값 대응 위한 딕셔너리
tag_names ={
    'addr1' : '주소',
    'areacode' : '지역',
    'cat1' : '대분류',
    'cat2' : '중분류',
    'cat3' : '소분류',
    'contenttypeid' : '장소유형',
    'sigungucode' : '시군구',
    'title' : '장소명',
    'BF' : '무장애 정보'
}

# 무장애 정보 태그용 딕셔너리
bf_tags ={
    'parking' : '주차',
    'route' : '대중교통',
    'publictransport' : '접근로',
    'ticketoffice' : '매표소',
    'promotion' : '홍보물',
    'wheelchair' : '휠체어',
    'exit' : '출입통로',
    'elevator' : '엘레베이터',
    'restroom': '화장실',
    'auditorium': '관람석',
    'room' : '객실',
    'handicapetc' : '지체장애 편의시설',
    'braileblock' : '점자블록',
    'helpdog' : '보조견동반',
    'guidehuman' : '안내요원',
    'audioguide' : '오디오 가이드',
    'bigprint' : '큰활자 홍보물',
    'brailepromotion' : '점자홍보물 및 점자표지판',
    'guidesystem' : '유도안내설비',
    'blindhandicapetc' : '시각장애 편의시설',
    'signguide' : '수화안내',
    'videoguide' : '영상자막안내',
    'hearingroom' : '청각 객실',
    'hearinghandicapetc' : '청각장애 편의시설',
    'stroller' : '유모차',
    'lactationroom' : '수유실',
    'babysparechair' : '유아용 보조의자',
    'infantsfamilyetc' : '영유아가족 기타상세',
}


# 지역, 서비스 코드값 대응 위한 csv 로드
geo_file = False
ser_file = False
try:
    geo_df = pd.read_csv("./search/resources/geo_code.csv", encoding='euc-kr')
    ser_df = pd.read_csv("./search/resources/service_code.csv", encoding='euc-kr')
    geo_file = True
    ser_file = True
except:
    print('err: code csv files do not exist')
    print(os.getcwd())
    
### 데이터 처리용 변수 -끝-


# x, y좌표 취합
def getGeoInfos(contentId):
    apiInfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
    req = tourReq('ETC', 'AppTest', apiInfo.mykey)
    req.addPara('contentId', contentId)
    req.addPara('mapinfoYN', 'Y')
    tmp = parseOne(req.makeReq(apiInfo.url, 'detailCommon'))
    result = getInfos(tmp)

    geo_dict = {'mapx':result.get('mapx'),'mapy':result.get('mapy'),'mlevel':result.get('mlevel')}

    return geo_dict