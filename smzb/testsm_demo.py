__author__ = 'wangxiao'


# 导入对应的库

from locust import HttpUser, TaskSet, task, HttpLocust, between
import os


# 任务类



class TestSouMi(HttpUser):
    wait_time = between(5, 30)

    @task
    def index_page(self):
        self.client.get("/")
        print("收米直播")


if __name__ == '__main__':
    print(os.getcwd())
    # os.system("locust -f testsm_demo.py --host=http://smzb.tv:66")