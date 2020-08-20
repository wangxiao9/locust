__author__ = 'wangxiao'

# 导入对应的库

from locust import HttpUser, task, between, TaskSet
import os
from random import choice


# 任务类

class TestLogin(TaskSet):
    def on_start(self):
        self.data = [{"account": "wangxiao@qq.com", "password": "123456"},
                     {"account": "tester06@qq.com", "password": "123456"},
                     {"account": "admin@admin.com", "password": "123456"},
                     {"account": "admin@admin.com", "password": "12334456"}
                     ]

    @task
    def to_login(self):
        with self.client.post("/v1/token", json=choice(self.data), catch_response=True) as response:
            res = response.json()
            if res['error_code'] == 0:
                response.success()
            else:
                response.failure(res['msg'])

    def on_stop(self):
        print("task结束")


class WebUser(HttpUser):
    tasks = [TestLogin]
    wait_time = between(2, 5)
    host = "http://127.0.0.1:5000"


if __name__ == '__main__':
    os.system("locust -f testsm_demo.py")
