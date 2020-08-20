import os

import jsonpath as jsonpath
from locust import User, task, events, constant
import time
import websocket
import ssl
import json
from random import choice

def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(request_type="[RECV]",
                                name=eventType,
                                response_time=total_time,
                                response_length=len(recvText))


class WebSocketClient(object):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    def connect(self, burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
        except websocket.WebSocketConnectionClosedException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='Connection is already closed', response_time=total_time, exception=e)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='TimeOut', response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="[Connect]", name='WebSocket', response_time=total_time, response_length=0)
        return self.conn

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class ApiUser(WebsocketUser):
    host = "wss://api.bbx.com"
    wait_time = constant(0)

    def on_start(self):
        # wss 地址
        self.url = 'wss://api.bbx.com/v1/ifcontract/realTime'
        self.data = ['{"action": "subscribe", "args": ["Ticker"]}', '{action: "ping"}']
        self.client.connect(self.url)
        self.client.send(choice(self.data))


    @task(1)
    def to_main(self):
        while True:
            # 消息接收计时
            start_time = time.time()
            recv = self.client.recv()
            total_time = int((time.time() - start_time) * 1000)

            # 为每个推送过来的事件进行归类和独立计算性能指标
            try:
                recv_j = json.loads(recv)
                eventType_s = jsonpath.jsonpath(recv_j, expr='$.eventType')
                eventType_success(eventType_s[0], recv, total_time)
            except websocket.WebSocketConnectionClosedException as e:
                events.request_failure.fire(request_type="[ERROR] WebSocketConnectionClosedException",
                                            name='Connection is already closed.',
                                            response_time=total_time,
                                            exception=e)
            except:
                print(recv)
                # 正常 OK 响应，或者其它心跳响应加入进来避免当作异常处理
                if 'ok' in recv:
                    eventType_success('ok', 'ok', total_time)

if __name__ == '__main__':
    os.system("locust -f locust_websocket.py")