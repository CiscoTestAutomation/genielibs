import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_log_buffer


class TestUnconfigureIpArpInspectionLogBuffer(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_log_buffer(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_log_buffer(device, 'logs')
        self.assertIsNone(result)
        device.configure(['no ip arp inspection log buffer logs'])