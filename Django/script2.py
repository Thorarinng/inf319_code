from script import PerformanceTester


pt = PerformanceTester()


for i in range(100):
    pt.readPosts()
    pt.result()