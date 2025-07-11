import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_vlan


class TestUnconfigureIpArpInspectionVlan(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_vlan(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_vlan(device, 10)
        self.assertIsNone(result)
        device.configure.assert_called_once_with(['no ip arp inspection vlan 10'])