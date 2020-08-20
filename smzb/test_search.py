__author__ = 'wangxiao'

import os

from locust import HttpUser, task, between, TaskSet


class SouMiSearch(TaskSet):
    @task
    def search(self):
        url = "/api/p/search/"
        body = {"keywords": "ceess"}
        with self.client.post(url, json=body) as response:
            print(response.text)


class WebUser(HttpUser):
    tasks = [SouMiSearch]
    wait_time = between(2, 5)
    host = "http://api.shoumilive.com:83"


if __name__ == '__main__':
    os.system("locust -f test_search.py")