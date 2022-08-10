import requests
import time

# url = 'http://127.0.0.1:8000/api/post/'

# myobj = {'comment': 'somevalue'}

# x = requests.get(url, data = myobj, headers=headers).json()

# print(x)

class PerformanceTester:
    def __init__(self) -> None:
        self.req = requests
        self.url = 'http://127.0.0.1:8000/api/'

        self.Bearer = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NzIzNTQ3LCJpYXQiOjE2NDU3MjM1NDcsImp0aSI6IjBiZjkxMjNiMDUxYTRiYTE4NTc3NTU3ZTQ0Y2RlOGFiIiwidXNlcl9pZCI6MX0.TRlHt5zQ_DUeycFO2ZPtN9ZcRmR93LpTKTjzhnChRT8'
        self.headers = {"Authorization": f"Bearer {self.Bearer}"}

    def __startTime(self):
        self.startTime = time.time()

    def __endTime(self):
        self.timeTaken = time.time() - self.startTime

    def result(self):
        print("--> %s seconds <--" % self.timeTaken)


    def readPosts(self):
        url = f"{self.url}post/" 

        self.__startTime()
        res = self.req.get(url,headers=self.headers).json()
        self.__endTime()
        
        print(len(res['posts']))
        print("--> reading posts <--")

    def writePost(self):
        url = f"{self.url}post/" 
        data ={"comment": "This is another post"}

        # self.__startTime()
        for i in range(100):
            time.sleep(1)
            for j in range(1000):
                res = self.req.post(url, data=data, headers=self.headers).json()
        # self.__endTime()

        print("--> writing post <--")


if __name__ == "__main__":
    '''
    Run this file script.py and then run script2.py to test read-speed while the backend deals 
    with 1000 write requests per second
    '''
    pt = PerformanceTester()

    # pt.writePost()
    pt.readPosts()
    pt.result()
