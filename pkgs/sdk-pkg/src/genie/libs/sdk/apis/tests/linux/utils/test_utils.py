import unittest
from unittest import mock
import ipaddress

from genie.libs.sdk.apis.linux.utils import get_valid_ipv4_address



class TestGetValidIpv4(unittest.TestCase):
    def test_get_valid_ipv4_addres(self):
        device = mock.Mock()
        ip = '127.0.0.1/16'
        self.assertEqual(get_valid_ipv4_address(device, ip), ipaddress.IPv4Address('127.0.0.1'))
        with self.assertRaises(ipaddress.AddressValueError):
            get_valid_ipv4_address(device, '123/234')
