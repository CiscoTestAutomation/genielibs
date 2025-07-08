import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_filter


class TestUnconfigureIpArpInspectionFilter(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_filter(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_filter(device, 'allowed_acl', '10')
        self.assertIsNone(result)
        device.configure.assert_called_once_with(['no ip arp inspection filter allowed_acl vlan 10'])