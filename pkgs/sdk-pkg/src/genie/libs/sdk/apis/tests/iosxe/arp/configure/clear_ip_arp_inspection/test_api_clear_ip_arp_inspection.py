import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import clear_ip_arp_inspection


class TestClearIpArpInspection(unittest.TestCase):

    def test_clear_ip_arp_inspection(self):
        device = Mock()

        device.execute = Mock()

        result = clear_ip_arp_inspection(device, 'statistics')

        self.assertIsNone(result)

        device.execute.assert_called_once_with("clear ip arp inspection statistics")
