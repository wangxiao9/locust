__author__ = 'wangxiao'

import os

from locust import HttpUser, TaskSet, task, between, User


class Main(TaskSet):
    @task(1)
    def to_main(self):
        url = "/ofm"
        self.client.get(url, name="打开系统登陆页面")

class MainUser(HttpUser):
    tasks = {Main: 2}
    wait_time = between(1000, 3000)
    host = "http://10.192.30.232/"


if __name__ == '__main__':
    os.system("locust -f test_sys.py")