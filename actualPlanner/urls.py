from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('plannerchoice/', views.plannerchoice, name ='plannerchoice'),
    path('createplan/', views.createplan, name ='createplan'),
    path('showplan/', views.showplan, name ='showplan'),
    path('cplan/', views.cplan, name='tst'),
    
]