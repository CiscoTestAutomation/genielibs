import time
from yang.connector import proto

class Service:
    def __init__(self, response):
        self.response = response

    def Get(self, *args, **kwargs):
        return self.response

    def Subscribe(self, *args, **kwargs):
        return [self.response]

    def Set(self, *args, **kwargs):
        resp = proto.gnmi_pb2.SetResponse()
        resp.timestamp = time.time_ns()
        return resp


class Gnmi:
    def __init__(self, response):
        self.response = response
        self.service = Service(response)


class Default:
    default = {'username': 'test', 'password': 'password'}


class Creds:
    credentials = Default()
    testbed = {}


class TestDevice:
    device = Creds()
    active_notifications = {}
    name = 'test'

    def __init__(self, response):
        self.gnmi = Gnmi(response)


class TestbedWithNtp:
    servers = {'ntp': {'server': "1.1.1.1"}}


class TestDeviceWithNtp(TestDevice):
    def __init__(self, response):
        super().__init__(response)
        self.device.testbed = TestbedWithNtp()
