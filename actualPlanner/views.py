from django.shortcuts import render
from django.http import HttpResponse, Http404



from .models import Planner

def index(request):
    return render(request, 'planner/index.html')

def plannerchoice(request):
    return render(request, 'planner/plannerchoice.html')

def createplan(request):
    return render(request, 'planner/createplan.html')

def showplan(request):
    return render(request, 'planner/showplan.html')
