from django.shortcuts import render
from .datas import *

def testview(request):
    df1 = basicTable()
    
    return render(request, 'collector/testview.html', {'df':df1})

