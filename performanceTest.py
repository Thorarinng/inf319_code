import datetime
from pickle import FALSE, TRUE
import requests
import json


tester = {
"email": "test0@test.test",
"password": "test0",
"password2": "test0",
"username": "test0",
"firstname": "test0",
"lastname": "test0",
"phoneNumber": "774-5566",
"imgURL": "IMAGE_URL"
}

mainTesterTen = {
    "email": "maintester-ten@test.test",
    "password": "maintester",
    "password2": "maintester",
    "username": "maintester-ten",
    "firstname": "maintester",
    "lastname": "maintester",
    "phoneNumber": "774-5566",
    "imgURL": "IMAGE_URL"
    }

mainTesterHundred = {
    "email": "maintester-hundred@test.test",
    "password": "maintester",
    "password2": "maintester",
    "username": "maintester-hundred",
    "firstname": "maintester",
    "lastname": "maintester",
    "phoneNumber": "774-5566",
    "imgURL": "IMAGE_URL"
    }

mainTesterThousand = {
    "email": "maintester-thousand@test.test",
    "password": "maintester",
    "password2": "maintester",
    "username": "maintester-thousand",
    "firstname": "maintester",
    "lastname": "maintester",
    "phoneNumber": "774-5566",
    "imgURL": "IMAGE_URL"
    }

testers = [mainTesterTen, mainTesterHundred, mainTesterThousand]

NAIVE_TYPE = "naive"
REST_TYPE = "REST"
GRAPHQL_TYPE = "graphql"

class Time:
    def __init__(self) -> None:
        self.s = None
        self.e = None

        self.tLis = []

    def start(self):
        self.s = datetime.datetime.now()

    def end(self):
        self.e = datetime.datetime.now()
        self.tLis.append(self.e-self.s)

    def time(self):
        return self.e - self.s

    def times(self):
        print("\n- All times -")
        for time in self.tLis:
            print(time)

class Users:
    def __init__(self) -> None:

        self.testers = []

    def getUsers(self,n):

        temp_tester = tester.copy()

        testers = []

        for i in range(1,n+1):
            i = str(i)
            prev = str(int(i) - 1)
            temp_tester['email'] = temp_tester['email'].replace(prev, i)
            temp_tester['password'] = temp_tester['password'].replace(prev, i)
            temp_tester['password2'] = temp_tester['password2'].replace(prev, i)
            temp_tester['username'] = temp_tester['username'].replace(prev, i)
            temp_tester['firstname'] = temp_tester['firstname'].replace(prev, i)
            temp_tester['lastname'] = temp_tester['lastname'].replace(prev, i)

            a = temp_tester.copy()

            testers.append(a)
        
        self.testers = testers
        # print(testers)
        return testers




class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

class APICommunication:
    def __init__(self, api_type) -> None:
        self.prefix = "http://localhost:8000/"
        self.isGraphql = False


        if api_type == NAIVE_TYPE:
            self.api_type = "api/naive"


        elif api_type == REST_TYPE:
            self.api_type = "api"
        

        elif api_type == GRAPHQL_TYPE:
            self.api_type = "api"
            self.isGraphql = True


        self.requests = requests

        # User token storing the userId and permission information
        self.token = ""

    def printStatusCode(self,res):
        print(f"Status code: {res.status_code}")

    def getPosts(self):

        if self.isGraphql:
            url = f"{self.prefix}graphql/"
            query = """query {
                allPosts {
                    posts {
                        id
                        comment
                        likeCount
                        }
                    }
            }"""

            r =  self.requests.post(url, json={"query": query}, auth=BearerAuth(self.token))
            data = json.loads(r.text)
            return data['data']['allPosts']

        else:
            url = f"{self.prefix}{self.api_type}/post/"
            r =  self.requests.get(url, auth=BearerAuth(self.token))

            return json.loads(r.text)

    def createPost(self,comment):
        url = f"{self.prefix}{self.api_type}/post/"
        r = self.requests.post(url,{'comment': comment},auth=BearerAuth(self.token))

        print(f"Status code: {r.status_code}")

    def createUser(self,user):
        url = f"{self.prefix}{self.api_type}/user/register/"

        r = self.requests.post(url,user)

        self.printStatusCode(r)

    def loginUser(self,user):
        url = f"{self.prefix}{self.api_type}/user/login/"

        r = self.requests.post(url,user)

        self.printStatusCode(r)

        return json.loads(r.text)

    def followUser(self,username):
        '''
        Makes main tester follow a specific user
        '''
        # url = f"{self.prefix}{self.api_type}/follow/{username}/"

        # r = self.requests.post(url,auth=BearerAuth(self.token))

        # self.printStatusCode(r)

        pass

    def __get_login_creds_main_tester(self,user):
        keys = ["email","password"]

        loginCreds = {}

        for key in keys:
            loginCreds[key] = user.get(key)

        return loginCreds


    def followMe(self,user,mainTestUser):
        '''
        Makes specific user follow a main tester
        '''
        loginCreds = self.__get_login_creds_main_tester(user)
        user = self.loginUser(loginCreds)

        # User that is going to follow
        token = user['tokens']['access']

        # User being followed
        username = mainTestUser['username']


        url = f"{self.prefix}{self.api_type}/follow/{username}"

        # Who gets followed? username user is followed 
        # who follows? the token owner
        r = self.requests.post(url,auth=BearerAuth(token))

        follow = json.loads(r.text)
        followingStatus = follow['isFollowing']


        if followingStatus:
            print(f"FollowingStatus: {followingStatus}")
        else:
            r = self.requests.post(url,auth=BearerAuth(self.token))

        self.printStatusCode(r)


    def getFollowers(self):
        url = f"{self.prefix}{self.api_type}/follow/followers/"

        r = self.requests.get(url,auth=BearerAuth(self.token))


        data = json.loads(r.text)
        
        return data
    
    def getFollowing(self):
        url = f"{self.prefix}{self.api_type}/follow/following/"

        r = self.requests.get(url,auth=BearerAuth(self.token))

        data = json.loads(r.text)
        
        return data



class PerformanceTester:
    def __init__(self,token,api_type) -> None:
        self.testers = Users().testers

        self.apc = APICommunication(api_type=api_type)
        self.apc.token = token
        self.t = Time()

        # Difference in terms of end and start (end - start) time.
        self.diff_time = None

    def getPosts(self):
        self.t.start()
        posts = self.apc.getPosts()
        self.t.end()
        self.diff_time = self.t.time()


        return posts

    def getFollowers(self):
        self.t.start()
        data = self.apc.getFollowers()
        self.t.end()
        self.t.time()
        return data

    def getFollowing(self):
        self.t.start()
        data = self.apc.getFollowing()
        self.t.end()
        self.t.time()
        return data



class TestDataGenerator():
    def __init__(self,api_type,n=10) -> None:
        self.n = n


        self.apc = APICommunication(api_type=api_type)

        self.users = Users().getUsers(self.n)

    def genXUsers(self):
        for user in self.users:
            self.apc.createUser(user)

    def genTenPosts(self):
        comment = "This is a test generated comment"
        
        for x in self.users:
            self.apc.createPost(comment)

def __get_login_creds_main_tester(mainTestUser):
    keys = ["email","password"]

    loginCreds = {}

    for key in keys:
        loginCreds[key] = mainTestUser.get(key)

    return loginCreds


def createMainTestUser(api_type, mainTestUser):
    print("Creating Main User..")
    apc = APICommunication(api_type=api_type)

    apc.createUser(mainTestUser)

def loginMainTestUser(api_type,mainTestUser):
    print("Logging in Main User..")
    apc = APICommunication(api_type=api_type)

    loginCreds = __get_login_creds_main_tester(mainTestUser)

    user = apc.loginUser(loginCreds)

    return user['tokens']['access'], user

def makeUsersFollowMainTester(mainTestUser,token,api_type,n=10):
    apc = APICommunication(api_type=api_type)
    apc.token = token

    users = Users().getUsers(n=n)


    for user in users:
        apc.followMe(user,mainTestUser)


# def generateNUsers(n,api_type):
#     tdg = TestDataGenerator(n=n,api_type=api_type)
#     # tdg.genTenPosts()
#     tdg.genXUsers()

def generateAPost(api_type,n=1000):
    '''
    For each user it creates a single post
    '''

    apc = APICommunication(api_type=api_type)

    users = Users().getUsers(n=n)

    count = 0
    for user in users:
        loginCreds = __get_login_creds_main_tester(user)
        user = apc.loginUser(loginCreds)
        
        # print(count)
        count += 1
        apc.token = user['tokens']['access']

        apc.createPost("Every user has a single post")




# api_type = REST_TYPE


# generateAPost(api_type)

# print()
# print(tokenTen)
# print()
# print(tokenHundred)
# print()
# print(tokenThousand)
# print()

# tokenTen, mainTesterTenUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterTen)
# tokenHundred, mainTesterHunderdUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterHundred)
# tokenThousand, mainTesterThousandUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterThousand)

# makeUsersFollowMainTester(mainTestUser=mainTesterTenUserInstance,token=tokenTen,api_type=api_type,n=10)
# makeUsersFollowMainTester(mainTestUser=mainTesterHunderdUserInstance,token=tokenHundred,api_type=api_type,n=100)
# makeUsersFollowMainTester(mainTestUser=mainTesterThousandUserInstance,token=tokenThousand,api_type=api_type,n=1000)

# makeUsersFollowMainTester(token=tokenTen,api_type=api_type,n=10)
# makeUsersFollowMainTester(token=tokenHundred,api_type=api_type,n=100)
# makeUsersFollowMainTester(token=tokenThousand,api_type=api_type,n=1000)

def perform_scalability_test(scalability_ns):
    print("--- SCALABILITY_TEST ---")
    for n, pt in scalability_ns.items():
        print()
        print()
        
        # Number of posts
        print(f"N-size: {n}")

        # followers = pt.getFollowers()['followers']
        # following = pt.getFollowing()['following']

        # followers_size = len(followers)
        # following_size = len(following)

        # print(f"\n- Followers: {followers_size}")
        # print(f"\n- Following: {following_size}")
        # print()

        posts = pt.getPosts()['posts']
        # print(posts)
        post_size = len(posts)
        print(f"\n- Posts: {post_size}")
        print()
        print()
        print()
        print()
        print()
        print()

def perform_load_test(load_ns):
    print("--- LOAD_TEST ---")
    print("starts...")
    # TODO: Load Testing
    users = 100
    time_sum = None
    total_times = 0
    for i in range(users):
        for n, pt in load_ns.items():
            
            # Number of posts
            # print(f"N-size: {n}")
            posts = pt.getPosts()['posts']

            if time_sum is None:
                time_sum = pt.diff_time
            else:
                time_sum += pt.diff_time
                
            total_times += 1
    
    average = time_sum / total_times
    print(f"Total Times: {total_times}")
    print(f"Average Time: {average}")


def perform_stress_test(stress_ns):
    print("--- STRESS_TEST ---")

    # Same amount of posts needed to perform the same test
    # However, four instances of the performanceTester.py run simultaneously
    perform_load_test(stress_ns)

# api_types = [NAIVE_TYPE, REST_TYPE,GRAPHQL_TYPE]
api_types = [GRAPHQL_TYPE]

for api_type in api_types:
    print(f"--- API-TYPE: {api_type} ---")

    createMainTestUser(api_type=api_type,mainTestUser=mainTesterTen)
    createMainTestUser(api_type=api_type,mainTestUser=mainTesterHundred)
    createMainTestUser(api_type=api_type,mainTestUser=mainTesterThousand)

    tokenTen, mainTesterTenUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterTen)
    tokenHundred, mainTesterHunderdUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterHundred)
    tokenThousand, mainTesterThousandUserInstance = loginMainTestUser(api_type=api_type,mainTestUser=mainTesterThousand)

    pt_ten = PerformanceTester(token=tokenTen,api_type=api_type)
    pt_hundred = PerformanceTester(token=tokenHundred,api_type=api_type)
    pt_thousand = PerformanceTester(token=tokenThousand,api_type=api_type)


    # TODO: Scalability Testing
    scalability_ns = {"10": pt_ten,"10 0": pt_hundred,"1000": pt_thousand}

    # TODO: Load Testing
    load_ns = {"10": pt_ten}

    # TODO: Stress Testing
    stress_ns = {"10": pt_ten}

    # perform_scalability_test(scalability_ns)
    perform_load_test(load_ns)
    # perform_stress_test(stress_ns)
