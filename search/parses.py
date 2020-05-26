# 지역, 서비스 코드 파서

import pandas as pd
import numpy as np
import re
import datetime

from .rq_class import *
from .search import findTag, parseAll

apinfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

def getCode(obj):
    result = {}
    for i in range(0, len(obj)):
        tmp = list(re.split('[<>]', str(obj[i])))
        while '' in tmp: tmp.remove('')
        result[findTag(tmp, 'name')] = findTag(tmp, 'code')
    return result


def geoCode(apinfo):
    # 대분류
    gcode_req = tourReq('ETC', 'AppTest', apinfo.mykey)
    g_req = gcode_req.makeReq(apinfo.url, 'areaCode')
    g1_dic = getCode(parseAll(g_req))

    result_tmp=[]
    for tags, codes in g1_dic.items():
        input_tmp=[]

        gcode_req2 = tourReq('ETC', 'AppTest', apinfo.mykey)
        gcode_req2.addPara('areaCode', codes)
        req2 =  gcode_req2.makeReq(apinfo.url, 'areaCode')
        g2_dic = getCode(parseAll(req2))

        for tag2, code2 in g2_dic.items():
            input_tmp.append(tags)
            input_tmp.append(codes)
            input_tmp.append(tag2)
            input_tmp.append(code2)
            # 리스트 단위로 행추가
            result_tmp.append(input_tmp)
            #
            input_tmp=[]
    
    df_geo = pd.DataFrame(result_tmp, columns=['city','city_code','sigungu','sigungu_code'])

    # CSV로 내보내기
    geo_code_date = datetime.datetime.today()
    geo_code_date = geo_code_date.strftime('%Y-%m-%d')
    df_geo.to_csv("resources/geo_code_{}.csv".format(geo_code_date), encoding='euc-kr')





def serviceCode(apinfo):

    # 대분류
    scode_req = tourReq('ETC', 'AppTest', apinfo.mykey)
    req_cat1 = scode_req.makeReq(apinfo.url, 'categoryCode')
    cat1_dic = getCode(parseAll(req_cat1))

    result_tmp=[]
    for tags, codes in cat1_dic.items():
        input_tmp = []

        # 중분류
        req2_tmp = tourReq('ETC', 'AppTest', apinfo.mykey)
        req2_tmp.addPara('cat1', codes)
        req2 = req2_tmp.makeReq(apinfo.url, 'categoryCode')
        cat2_dic = getCode(parseAll(req2))

        # 소분류
        for tag2, code2 in cat2_dic.items():
            req2_tmp.addPara('cat2', code2)
            req3 = req2_tmp.makeReq(apinfo.url, 'categoryCode')
            cat3_dic = getCode(parseAll(req3))

            for tag3, code3 in cat3_dic.items():
                input_tmp.append(tags)
                input_tmp.append(codes)
                input_tmp.append(tag2)
                input_tmp.append(code2)
                input_tmp.append(tag3)
                input_tmp.append(code3)

                # 리스트단위로 행추가
                result_tmp.append(input_tmp)

                #
                input_tmp = []
    df_cat = pd.DataFrame(result_tmp, columns=['tag1','code1','tag2','code2','tag3','code3'])

    # CSV로 내보내기
    service_code_date = datetime.datetime.today()
    service_code_date = service_code_date.strftime('%Y-%m-%d')
    df_cat.to_csv("resources/service_code_{}.csv".format(service_code_date), encoding='euc-kr')


# 업데이트 여부
up_scode = False
up_gcode = False

if up_scode:
    serviceCode(apinfo)
    print('done!')

if up_gcode:
    geoCode(apinfo)
    print('done!')

                
                






