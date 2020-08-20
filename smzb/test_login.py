__author__ = 'wangxiao'

import json
import os

from locust import HttpUser, between, task
from random import randint

"""
1. 实现登陆基本功能，输出相应，脚本通
2. 多用户实现随机登陆
3. 添加初始化方法on_start: 每个用户只运行一次
4. 添加检查点： catch_responses = True
"""


# 登陆脚本

class TestFunction(HttpUser):
    wait_time = between(5, 10)

    # @task
    # def to_login(self):
    #     data = {"account": "wangxiao@qq.com", "password": "123456"}
    #     res = self.client.post("/v1/token", json=data)
    #     print(res.text)

    # @task
    # def to_login(self):
    #     data = [{"username": "admin123456", "password": "admin123456", "savePassword": False, "loginType": "dpp",
    #             "loginApplication": "dpp"},
    #             {"username": "wangxiao", "password": "ofm123##", "savePassword": False, "loginType": "dpp",
    #              "loginApplication": "dpp"},
    #             {"username": "wangxiao2", "password": "ofm123##", "savePassword": False, "loginType": "dpp",
    #              "loginApplication": "dpp"}
    #             ]
    #     randindex = randint(1, 10) % len(data)
    #     res = self.client.post("/gateway/cas/inner/login", json=data[randindex])
    #     print(data[randindex]['username'])
    #     print(res.text)
    def on_start(self):
        self.loginData = [{"username": "admin123456", "password": "admin123456", "savePassword": False, "loginType": "dpp",
                 "loginApplication": "dpp"},
                {"username": "wangxiao", "password": "ofm123##", "savePassword": False, "loginType": "dpp",
                 "loginApplication": "dpp"},
                {"username": "wangxiao2", "password": "123456", "savePassword": False, "loginType": "dpp",
                 "loginApplication": "dpp"}
                ]

    @task
    def to_login(self):
        randindex = randint(1, 10) % len(self.loginData)
        with self.client.post("/gateway/cas/inner/login", json=self.loginData[randindex], catch_response=True) as response:
            json_str = response.json()
            code = json_str["code"]
            if code == 0:
                response.success()
            else:
                response.failure('login failure')

        # print(res.text)
        # print(type(res.text))
        # print()

if __name__ == '__main__':
    os.system("locust -f test_login.py --host=http://10.192.30.232")
