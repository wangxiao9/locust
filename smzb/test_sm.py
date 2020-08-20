__author__ = 'wangxiao'

# 导入对应的库
import json
import random
import string
import time

import gevent
from locust import HttpUser, task, between, TaskSet, events
import os
from random import choice
import websocket
import gzip


# 任务类

class TestLogin(TaskSet):

    def to_login(self, data):
        res = self.client.post("/api/p/login/login/pwd", json=data)
        data = res.json()
        uuid = data['data']['uuid']
        return uuid

    def on_start(self):
        ws = websocket.WebSocket()
        ws.connect('ws://im.shoumilive.com:3102/sub')
        self.ws = ws
        gevent.spawn(self._receive)

    def _receive(self):
        while True:
            res = self.ws.recv()
            data = json.loads(res)
            print(data)
            end_at = time.time()
            events.request_success.fire(
                request_type='WebSocket Recv',
                name='test/ws/recv',
                response_time=int((time.time() - end_at) * 1000),
                response_length=len(res),
            )


    @task
    def enter_room(self):
        while True:
            result = self.ws.receive()
            result_1 = json.loads(result)
            print(result_1)

    # @task
    # def to_send_msg(self):
    #     uuid = self.to_login(self.data)
    #     body = {"room": 93113, "type": 2, "content": "路过"}
    #     res = self.client.post("/api/p/user/send/" + uuid, data=body)
    #     print(res.text)

    def on_stop(self):
        self.ws.close()


# class WebUser(HttpUser):
#     tasks = [TestLogin]
#     wait_time = between(2, 5)
#     # host = "http://api.shoumilive.com:83"
#     host = "im.shoumilive.com:3102"

class WebUser(HttpUser):
    tasks = [TestLogin]
    wait_time = between(2, 5)
    # host = "http://api.shoumilive.com:83"
    host = "im.shoumilive.com:3102"


if __name__ == '__main__':
    os.system("locust -f test_sm.py")
