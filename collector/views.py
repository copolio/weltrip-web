from django.shortcuts import render
from .datas import *

def testview(request):
    df1 = basicTable()
    df2 = userHisTable('hilee')
    df3 = userHisTable('hyein')
    df4 = userHisTable('islandb')
    
    print(df2)
    print(df3)
    print(df4)

    return render(request, 'collector/testview.html', {'df':df1, 'df2':df2, 'df3':df3, 'df4':df4})

