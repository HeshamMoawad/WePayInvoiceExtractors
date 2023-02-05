import threading as thr
import requests as req
import numpy as np
from MyPyQt5 import QObject
# url = "https://proxylist.geonode.com/api/proxy-list?limit=1000&page=1&sort_by=lastChecked&sort_type=desc"

# res = req.get("https://proxylist.geonode.com/api/proxy-list?limit=500")
# ids = res.json()['data']
# print(type(ids))


# proxy = {
#     'http': 'http://41.33.47.147:1981', 
#     'https': 'https://41.33.47.147:1981'
#     }
# {'http':f'http://','https':f'https://'}

class ProxyFilterAPI(QObject):
    def __init__(self,threadCount:int,testingURL,header,jsondata) -> None:
        self.APIurl = "https://proxylist.geonode.com/api/proxy-list?limit=500"
        self.Proxies = []  # good proxies 
        self.ThreadCount = threadCount
        self.Threads = []
        self.Errors = []
        self.ProxiesList = [] # All Proxies
        self.Header = header
        self.Jsondata = jsondata
        self.TestingURL = testingURL
        super().__init__()

    def getProxiesListFromWeb(self):
        res = req.get(
            url=self.APIurl,
            timeout=10 ,
            )
        ids = res.json()['data']
        for id in ids :
            ip_port = f"{id['ip']}:{id['port']}"
            proxy = {'http':f'http://{ip_port}','https':f'https://{ip_port}'}
            self.ProxiesList.append(proxy)
        

    def prepareProxies(self):
        self.RequestThread = thr.Thread(target=self.getProxiesListFromWeb)
        self.RequestThread.start()


    def testFunction(self,proxylist):
        for proxy in proxylist :
            s = req.Session()
            s.proxies = proxy
            s.headers = self.Header
            try:
                res = req.post(
                    url = self.TestingURL,
                    json = self.Jsondata ,
                )
                self.Proxies.append(proxy)
                #print(f'Good Proxy Found -> {proxy}')
            except Exception as e:
                self.Errors.append(e)


    def MultiThreadingRequest(self):
        self.RequestThread.join()
        Proxieslists = np.array_split(self.ProxiesList,self.ThreadCount)
        for proxyList in Proxieslists:
            task1 = thr.Thread(
                target = self.testFunction ,
                args=(proxyList,)
            )
            task1.start()

    def wait(self):
        for task in self.Threads :
            task.join()
            
        print("All Tasks End")
        print(f"ProxyFilter Result is -> {self.Proxies}\nYou Can Access With calling ProxyFilterAPI.Proxies")




    







