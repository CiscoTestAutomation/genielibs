import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import clear_arp_cache


class TestClearArpCache(unittest.TestCase):

    def test_clear_arp_cache(self):
        device = Mock()

        device.execute = Mock()

        result = clear_arp_cache(device)
        self.assertIsNone(result)
        device.execute.assert_called_with("clear arp-cache")

        result = clear_arp_cache(device, ip_address='1.1.1.1', vrf='red')
        self.assertIsNone(result)
        device.execute.assert_called_with("clear arp-cache vrf red 1.1.1.1")

        result = clear_arp_cache(device, ip_address='1.1.1.1')
        self.assertIsNone(result)
        device.execute.assert_called_with("clear arp-cache 1.1.1.1")
        result = clear_arp_cache(device, interface='Gi1/0/1')
        self.assertIsNone(result)
        device.execute.assert_called_with("clear arp-cache interface Gi1/0/1")
