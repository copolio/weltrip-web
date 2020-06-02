# class def
from search.search import *
from search.rq_class import *


class Node: # node: 장소 단위(1개 장소)
    
    def __init__(self):
        self.item = {'siteId':'', 'siteName':'', 'siteTime':'', 'siteType':1,}
    # type value(int): 
    # 0 - start point, 1 - mid point, 2 - end point

    def modiNode(self, key, value):
        self.item[key] = value
    
    def setTime(self, time):
        self.item['siteTime'] = time
    
    def setEdPoint(self):
        # setting a node to end-point
        self.item['siteType'] = int(2)

    def getSiteName(self, Id):
        api_tmp = ApiInfo('1a%2FLc1roxNrXp8QeIitbwvJdfpUYIFTcrbii4inJk3m%2BVpFvZSWjHFmOfWiH9T7TMbv07j5sDnJ5yefVDqHXfA%3D%3D', 'http://api.visitkorea.or.kr/openapi/service/rest/KorWithService/')
        tour_tmp = tourReq('ETC', 'AppTest', api_tmp.mykey)
        tour_tmp.addPara('contentId', Id)
        tour_tmp.addPara('defaultYN', 'Y')
        req_tmp = tour_tmp.makeReq(api_tmp.url, 'detailCommon')

        tmp = requests.get(req_tmp)
        soup = BeautifulSoup(tmp.content, 'html.parser')
        data = str(soup.find_all('title'))
        name = getInfos(data).get('title')

        self.item['siteName'] = name
    
    pass



class userPlan(Node): # Node로 이루어진 리스트 형태

    def __init__(self):
        self.plan = []
        self.userId = ''
    
    def addNode(self, Node):
        self.plan.append(Node)
    
    def delNode(self, NodeId):
        for i in range(0, len(self.plan)):
            tmp = self.plan[i]
            if tmp.item.get('siteId') == NodeId:
                pos = i
                break
        del self.plan[pos]
    
    def getString(self):
        string = ''
        for elm in self.plan:
            string += '{0}:{1}&'.format(elm.item.get('siteId'), elm.item.get('siteTime'))
        return string

    pass