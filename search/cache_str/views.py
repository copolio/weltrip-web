from django.shortcuts import render, get_object_or_404, redirect




from django.http import HttpResponse
from .models import SearchMeta, SearchObj
from .forms import searchForm

import datetime


from .search import *
from .rq_class import *



# 결과 상세보기 표출
def s_detail(request):
    if 'contentId' in request.POST and request.POST['contentId']:
        contentId = request.POST['contentId']
        contentTypeId = request.POST['contentTypeId']

        metaInfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
        
        infos = searchDetails(contentId, contentTypeId, metaInfo)




        return render(request, 'search/search_detail.html', {'C_id':contentId, 'T_id':contentTypeId, 'Infos':infos})
        
    
        # 이전 페이지에서 post방식으로 장소id, 타입id를 받아올 경우
        

        # 정보 조회
        
    


# 검색 결과표출
def k_search(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        metaInfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        if form.is_valid():
            SearchMeta = form.save(commit=False)
            SearchMeta.user = request.user
            SearchMeta.date = datetime.datetime.today()
            SearchMeta.save()

            # 결과 처리
            k_result = searchByKeyword(SearchMeta.key, metaInfo)
            searchObj = SearchObj()
            searchObj.key = SearchMeta.key
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
            # 무장애정보 추가조회
            metaInfo.setUrl('http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
            for elm in details:
                bfinfo = searchBF(elm['contentid'], metaInfo)
                elm['BF'] = bfinfo
            

            # 결과 페이지로 이동
            return render(request, 'search/search_result.html', {'SearchObj':searchObj, 'SearchMeta':SearchMeta, 'details': details, 'tag_names':tag_names, 'bf_tags':bf_tags,})
    
    else:
        form = searchForm()
        return render(request, 'search/search_test.html', {'form':form})

