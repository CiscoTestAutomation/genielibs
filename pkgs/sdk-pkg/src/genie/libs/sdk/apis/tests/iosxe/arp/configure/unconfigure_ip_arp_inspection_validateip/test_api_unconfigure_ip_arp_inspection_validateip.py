import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_validateip


class TestUnconfigureIpArpInspectionValidateip(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_validateip(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_validateip(device, 'src-mac')
        self.assertIsNone(result)
        device.configure(['no ip arp inspection validate src-mac'])