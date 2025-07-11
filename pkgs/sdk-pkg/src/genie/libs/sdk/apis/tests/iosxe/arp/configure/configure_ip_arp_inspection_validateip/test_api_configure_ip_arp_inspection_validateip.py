import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_validateip


class TestConfigureIpArpInspectionValidateip(unittest.TestCase):

    def test_configure_ip_arp_inspection_validateip(self):
        device = Mock()
        device.configure = Mock()
        result = configure_ip_arp_inspection_validateip(device, 'src-mac')
        self.assertIsNone(result)
        device.configure.assert_called_once_with(['ip arp inspection validate src-mac'])