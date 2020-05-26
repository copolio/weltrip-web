# plan module
from .plans_class import *
from .models import Planner
import datetime

# DB에서 해당 유저의 일정표들을 불러온다(조회)
def callPlan(userId):
    pass


# 새 일정표 추가
def newPlan(userId, planName):
    newplan = Planner(user = userId, date = datetime.datetime.today(), contents='', title=planName)
    newplan.save()
    pass


# contents(text field) -> plan variable for this module
def toPlan(userId):
    pass

