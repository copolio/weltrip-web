# plan module
from .plans_class import *
from .models import Planner
import datetime


# DB에서 해당 유저의 일정표들을 불러온다(조회)
def callPlans(userId):
    result_tmp = Planner.objects.filter(user=userId).values()
    return result_tmp
    
# 선택된 pk를 가진 일정표를 불러온다(조회)
def callPlan(pk):
    selected_plan = Planner.objects.get(id=pk)
    return selected_plan

# 새 일정표 추가
def newPlan(userId, planName):
    newplan = Planner(user = userId, date = datetime.datetime.today(), contents='', title=planName)
    newplan.save()
    pass










##DB상 Plan의 Contents필드(텍스트 필드, 최대길이 제한없음) 규격:
#
# 컨텐츠ID:체류시간&컨텐츠ID:체류시간& ... 컨텐츠ID:체류시간&



# contents(text field) -> plan variable for this module
def toPlan(planContents):
    # 빈 userPlan 객체 생성
    plan_output = userPlan()

    # 노드별로 분해
    tmp_nodes = planContents.split('&')

    # 노드 내에서 ID, 체류시간 분해
    for nodes in tmp_nodes:
        if nodes == '':
            break # 마지막 노드까지 완료

        tmp_info = nodes.split(':')
        
        # 노드 객체 생성
        new_node = Node()
        new_node.modiNode('siteId', str(tmp_info[0]))
        new_node.getSiteName(str(tmp_info[0]))
        new_node.setTime(tmp_info[1])

        # userPlan에 노드 추가
        plan_output.addNode(new_node)
    
    try:
        return plan_output
    except:
        return None
    


