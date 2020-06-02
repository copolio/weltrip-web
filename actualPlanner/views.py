from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404



from .models import Planner

def index(request):
    return render(request, 'planner/index.html')

def plannerchoice(request):
    return render(request, 'planner/plannerchoice.html')

def createplan(request):
    if 'pk_del' in request.POST and request.POST['pk_del']:
        target_id = request.POST.get('pk_del')
        target = Planner.objects.get(id=target_id)
        target.delete()

        user_input = request.user
        user_output = callPlans(user_input)
        return render(request, 'planner/createplan.html', {'plan_list':user_output})


    if request.user or user:
        user_input = request.user
        user_output = callPlans(user_input)
        return render(request, 'planner/createplan.html', {'plan_list':user_output})

        

    else:
        return render(request, 'planner/createplan.html')

def makeplanid(request):

    if 'new_plan_title' in request.POST and request.POST:
        new_title = request.POST.get('new_plan_title')
        Planner(date = datetime.datetime.today(), user = request.user, title = new_title, contents='').save()

        user_input = request.user
        user_output = callPlans(user_input)
        return render(request, 'planner/createplan.html', {'plan_list':user_output})
    else:
        return render(request, 'planner/makeplanid.html')
   

def showplan(request):
    return render(request, 'planner/showplan.html')


def reviseplan(request):
    # 선택된 일정표 불러오기
    if 'pk_userplan' in request.POST and request.POST['pk_userplan']:
        pk_input = request.POST.get('pk_userplan')
        pk_output = callPlan(pk_input)

        # 객체 생성
        plan_output = toPlan(pk_output.contents)
        plan_output.userId = pk_output.user

        if 'siteAdded' in request.POST and request.POST['siteAdded']:
            target_id = request.POST.get('siteAdded')
            target = Planner.objects.get(id=pk_input)
            target.contents = target.contents + '{0}:60&'.format(target_id)
            target.save()

            pk_output = callPlan(pk_input)
            plan_output = toPlan(pk_output.contents)
            plan_output.userId = pk_output.user
            
            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

        if 'sitetoDel' in request.POST and request.POST['sitetoDel']:
            target_id = request.POST.get('sitetoDel')
            target = Planner.objects.get(id=pk_input)
            plan_output.delNode(target_id)
            target.contents = plan_output.getString()
            target.save()

            pk_output = callPlan(pk_input)
            plan_output = toPlan(pk_output.contents)
            plan_output.userId = pk_output.user

            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

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
            return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'site_searched':results_list, 'pk_userplan':pk_input,})
        
        return render(request, 'planner/reviseplan.html', {'plan_slct': plan_output, 'pk_userplan':pk_input,})

    else:
        return render(request, 'planner/reviseplan.html')

def rankplan(request):
    return render(request, 'planner/rankplan.html')




from search.search import *
from .u_plans import *

def viewplan(request):
    if 'id_userplan' in request.POST and request.POST['id_userplan']:
        user_input = request.POST['id_userplan']
        user_output = callPlans(user_input)
        return render(request, 'planner/viewplan.html', {'plan_list':user_output})

    elif 'pk_userplan' in request.POST and request.POST['pk_userplan']:
        pk_input = request.POST['pk_userplan']
        pk_output = callPlan(pk_input)

        # 객체 생성부
        plan_output = toPlan(pk_output.contents)
        plan_output.userId = pk_output.user
        
        return render(request, 'planner/viewplan.html', {'plan_slct':plan_output})

    else:
        return render(request, 'planner/viewplan.html')


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
    if 'siteAdded' in request.POST and request.POST['siteAdded']:
        target_id = request.POST.get('siteAdded')
        target = Planner.objects.get(id=3)
        target.contents = target.contents + '{0}:60&'.format(target_id)
        target.save()
        return render(request, 'planner/cp_createplan.html')

    else:
        return render(request, 'planner/cp_createplan.html')


