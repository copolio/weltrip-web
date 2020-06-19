from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from planner.forms import searchForm
from actualPlanner.models import Rating
from actualPlanner.views import *
from actualPlanner.u_plans import *
from search.models import SearchMeta, SearchObj
from search.search import *
from search.rq_class import *

import datetime 

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} 님 환영합니다!')
            return redirect('profile_setting')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    appinfo = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D',
                        'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
    
    dis_ratings = Rating.objects.filter(userRated=request.user).count()
    if (dis_ratings != 0) :
        sites = randomSites(8, True, appinfo)
    else :
        sites = initialSites(8, True, appinfo)

    # sites = randomSites(8, True, appinfo)
    sites1 = sites[0:4]
    sites2 = sites[4:8]
    
    if 'ratings' in request.POST and (request.POST['ratings'] != '{}'):
        print(request.POST['ratings'])
        dis_user = Profile.objects.get(user=request.user)
        datas = toDict(request.POST.get('ratings'))
        dis_type = dis_user.disability
        pre_type = dis_user.preference
        user_name = request.user

        api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D','http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')

        preference_types = (
            ('A0101', '자연관광지'),
            ('A0102', '관광자원'),
            ('A0201', '역사관광지'),
            ('A0202', '휴양관광지'),
            ('A0203', '체험관광지'),
            ('A0204', '산업관광지'),
            ('A0205', '건축/조형물'),
            ('A0206', '문화시설'),
            ('A0207', '축제'),
            ('A0208', '공연/행사'),
            )

        for key, value in datas.items():

            tour_tmp = tourReq('ETC', 'AppTest', api_tmp.mykey)
            tour_tmp.addPara('contentId', key)
            tour_tmp.addPara('catcodeYN', 'Y')
            tour_tmp.addPara('defaultYN', 'Y')
            req_tmp = tour_tmp.makeReq(api_tmp.url, 'detailCommon')

            tmp = requests.get(req_tmp)
            soup = BeautifulSoup(tmp.content, 'html.parser')

            title_tmp = str(soup.find_all('title'))
            cat_tmp = str(soup.find_all('cat2'))

            site_id = key
            site_grade = int(value)
            site_name = getInfos(title_tmp).get('title')
            cat_value = getInfos(cat_tmp).get('cat2')
            cat_value_list = cat_value.split(', ')

            for i in range(len(cat_value_list)):
                for j in preference_types:
                    if j[0] == cat_value_list[i]:
                        cat_value_list[i] = j[1]
            cat_value = ', '.join(cat_value_list)

            # db 저장부
            Rating(contentId=site_id, contentName=site_name, contentType=cat_value,
                    userRated=user_name, userDType=dis_type, userPType=pre_type, grade=site_grade).save()
        
        messages.success(request, '선호도가 반영되었습니다!')
        return redirect('profile')

    else:
        return render(request, 'users/profile.html', {'random1': sites1, 'random2': sites2, })


@login_required
def profile_update(request):
    # to see if our forms are valid. if they are, save
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'{username}님의 프로필 수정이 반영되었습니다.')
            return redirect('profile') # to profile page
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    # u_form과 p_form을 template에 pass하자 to access these forms
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'users/profile_update.html', context)

@login_required
def profile_setting(request):
    # to see if our forms are valid. if they are, save
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'{username}님의 회원가입이 완료되었습니다. 아래 여행지들을 평가하면 Weltrip이 {username}님의 취향에 맞게 검색 결과를 보여줄 거예요!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form,
    }
    return render(request, 'users/profile_setting.html', context)
