from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='planner-home'),

]