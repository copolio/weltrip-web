


class tourReq:

    def __init__(self, os, app, key):
        self.necPara = {'MobileOS':str(os), 'MobileApp':str(app), }
        self.myKey = key
    
    def makeReq(self, url, des):
        self.tmp_req = url+des+'?'
        self.tmp_req += 'ServiceKey='+self.myKey

        for key, value in self.necPara.items():
            self.tmp_req += '&'+key+'='+str(value)
        
        return self.tmp_req
    
    def setKey(self, new_key):
        self.mykey = new_key

    def addPara(self, key, value):
        self.necPara[key] = value

    def modiPara(self, key, new_value):
        self.necPara[key] = new_value


class ApiInfo:
    
    def __init__(self, key, url):
        self.mykey = key
        self.url = url
    
    def setUrl(self, new_url):
        self.url = new_url
        