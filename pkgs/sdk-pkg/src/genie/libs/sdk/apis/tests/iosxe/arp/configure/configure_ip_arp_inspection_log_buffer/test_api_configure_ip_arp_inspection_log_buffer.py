import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_log_buffer


class TestConfigureIpArpInspectionLogBuffer(unittest.TestCase):

    def test_configure_ip_arp_inspection_log_buffer(self):
        device = Mock()
        device.configure = Mock()
        result = configure_ip_arp_inspection_log_buffer(device, 'logs', 20, 30)
        self.assertIsNone(result)
        device.configure(['ip arp inspection log buffer logs 20 30'])