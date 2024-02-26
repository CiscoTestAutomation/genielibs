import unittest
from unittest import mock
from genie.libs.sdk.apis.linux.get import  get_ip_route_for_ipv4


class TestGetIpRoute(unittest.TestCase):
    
    def test_get_ip_route_for_ipv4(self):
        device =mock.Mock()
        device.execute.return_value = '127.0.0.1 via 1.1..1 dev example src 127.0.0.0 uid 1000 \r\n    cache'
        self.assertEqual(get_ip_route_for_ipv4(device, '127.0.0.1'), '127.0.0.0')