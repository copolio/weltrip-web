from django.urls import path

from . import views

urlpatterns = [
    path('', views.k_search, name='k_search'),
    path('search_detail.html', views.s_detail, name='s_detail'),

]