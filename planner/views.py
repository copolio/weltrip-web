from django.shortcuts import render, redirect
from django.http import HttpResponse




# 검색 모듈과 연결 - 작성자:이혜인
from .forms import searchForm
from search.models import SearchMeta, SearchObj
from search.search import *
from search.rq_class import *
from collector.datas import basicTable
import datetime 


def home(request):

    # 인기장소 표출 - 작성자: 이혜인
    appinfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
    sites = popularSites(8, True, appinfo)
    sites1 = sites[0:4]
    sites2 = sites[4:8]


    return render(request, 'planner/home.html', {'popular1': sites1, 'popular2' : sites2,})

"""
def pop_sites(request):
    if request.method == 'POST':
        if request.POST['pop_title']:

            metaInfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

            meta = SearchMeta(key = request.POST['pop_title'], user = request.user, date = datetime.datetime.today())
            k_result = searchByKeyword(meta.key, metaInfo)
            searchObj = SearchObj()
            searchObj.key = meta.key
            searchObj.content = k_result

            # 상세페이지 출력 위한 결과 처리
            details = []
            for elm in k_result:
                tmp = getInfos(elm)
                details.append(tmp)
            details = checkInfos(details, 'title')
            for elm in details:
                findGeo(geo_df, elm)
                findSer(ser_df, elm)

            # 무장애정보 조회
            metaInfo.setUrl('http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
            for elm in details:
                bfinfo = searchBF(elm['contentid'], metaInfo)
                elm['BF'] = bfinfo

            # 결과 페이지로 이동
            return render(request, 'search/search_result.html', {'SearchObj':searchObj, 'SearchMeta':meta, 'details': details, 'tag_names':tag_names, 'bf_tags':bf_tags,})
    else:
        return redirect('planner/home.html')
"""


def connect_search(request):
    if request.method == 'POST':
        print(request.POST)
        form = searchForm(request.POST)
        metaInfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        if not (request.POST.get('keyword','') == ''):
            
            meta = SearchMeta(key = request.POST['keyword'], user = request.user, date = datetime.datetime.today())
            meta.save()

            # 결과 처리
            k_result = searchByKeyword(meta.key, metaInfo)
            searchObj = SearchObj()
            searchObj.key = meta.key
            searchObj.content = k_result

            # 상세페이지 출력 위한 결과 처리
            details = []
            for elm in k_result:
                tmp = getInfos(elm)
                details.append(tmp)
            details = checkInfos(details, 'title')
            rating_tmps = basicTable()

            for elm in details:
                # 각종 코드 한글명으로 치환
                findGeo(geo_df, elm)
                findSer(ser_df, elm)

                # 평점 데이터 조회
                try:
                    elm['rating_count'] = rating_tmps.at['_count_', str(elm.get('contentid'))]
                    elm['rating_avr'] = round(rating_tmps.at['_average_', str(elm.get('contentid'))], 2)
                except:
                    elm['rating_count'] = '0'
                    elm['rating_avr'] = '0'

            # 무장애정보 조회
            metaInfo.setUrl('http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
            for elm in details:
                bfinfo = searchBF(elm['contentid'], metaInfo)
                elm['BF'] = bfinfo

            # 결과 페이지로 이동
            return render(request, 'search/search_result.html', {'SearchObj':searchObj, 'SearchMeta':meta, 'details': details, 'tag_names':tag_names, 'bf_tags':bf_tags,})
    
    else:
        form = searchForm()
        return render(request, 'planner/home.html', {'form':form})