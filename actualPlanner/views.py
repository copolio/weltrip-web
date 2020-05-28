from django.shortcuts import render
from django.http import HttpResponse, Http404



from .models import Planner

def index(request):
    return render(request, 'planner/index.html')

def plannerchoice(request):
    return render(request, 'planner/plannerchoice.html')

def createplan(request):
    return render(request, 'planner/createplan.html')

def makeplanid(request):
    return render(request, 'planner/makeplanid.html')


from search.search import *

def cplan(request):
    if 'search-key' in request.POST and request.POST['search-key']:
        siteKey = request.POST['search-key']
        print(siteKey)
        api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        results_tmp = searchByKeyword(siteKey, api_tmp)
        print(results_tmp)
        results_list = []
        for elm in results_tmp:
            elm_tmp = getInfos(elm)
            dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid')}
            results_list.append(dic_tmp)
        # output_list = checkInfos(result_list, 'title')
        
        print(results_list)
        return render(request, 'planner/cp_createplan.html', {'site_searched':results_list})

    else:
        return render(request, 'planner/cp_createplan.html')

def reviseplan(request):
    if 'search-key' in request.POST and request.POST['search-key']:
        siteKey = request.POST['search-key']
        print(siteKey)
        api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        results_tmp = searchByKeyword(siteKey, api_tmp)
        print(results_tmp)
        results_list = []
        for elm in results_tmp:
            elm_tmp = getInfos(elm)
            dic_tmp = {'title':elm_tmp.get('title'), 'addr':elm_tmp.get('addr1'), 'contentId':elm_tmp.get('contentid')}
            results_list.append(dic_tmp)
        # output_list = checkInfos(result_list, 'title')
        
        print(results_list)
        return render(request, 'planner/reviseplan.html', {'site_searched':results_list})

    else:
        return render(request, 'planner/reviseplan.html')

def rankplan(request):
    return render(request, 'planner/rankplan.html')

def miniSearch(request):
    return render(request, 'planner/mini_search.html')

def showplan(request):
    return render(request, 'planner/showplan.html')