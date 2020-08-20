__author__ = 'wangxiao'


from locust import HttpUser, task


class create_task(HttpUser):

    def get_function(self):
        res = self.client.get("http://10.192.30.232/gateway/ofm-om/shiftfunction/functions/list/1/4/v1")
        function_id = res.json()['data'][0]["id"]
        return function_id


    def get_user(self):
        res = self.client.get("http://10.192.30.232/gateway/ofm-om/shiftfunction/functions/list/1/4/v1")
        user_id = res.json()["data"][0]["id"]
        return user_id

    @task
    def create_task(self):
        data = {"taskname":"test","shiftfunctionid":self.get_function(),"responsible":11453,"fleetnodename":"Power Plant c","tasktypeid":1,"nextexecution":1597939200000,"description":"eee","shiftlogid":303,"shifttypeid":null,"cronexpression":"0 0 0 */1 * ?","periodbase":1,"timezoneoffset":8,"executiontype":1,"durationtype":3,"endtime": "null","starttime":"1597852800000","noticetimeinterval":0,"documentfiles":[]}