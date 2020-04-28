from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='planner-home'),
    path('profile/', views.profile, name='planner-profile'),
]