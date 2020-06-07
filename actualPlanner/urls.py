from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('plannerchoice/', views.plannerchoice, name ='plannerchoice'),
    path('createplan/', views.createplan, name ='createplan'),
    path('makeplanid/', views.makeplanid, name ='makeplanid'),
    path('showplan/', views.showplan, name ='showplan'),
    path('cplan/', views.cplan, name='cplan'),
    path('viewplan/', views.viewplan, name='tst2'),
    path('reviseplan/', views.reviseplan, name='reviseplan'),
    path('rankplan/', views.rankplan, name='rankplan'),
    
]