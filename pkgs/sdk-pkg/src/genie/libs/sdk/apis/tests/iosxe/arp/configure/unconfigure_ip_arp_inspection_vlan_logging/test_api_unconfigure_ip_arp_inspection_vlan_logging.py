import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import unconfigure_ip_arp_inspection_vlan_logging


class TestUnconfigureIpArpInspectionVlanLogging(unittest.TestCase):

    def test_unconfigure_ip_arp_inspection_vlan_logging(self):
        device = Mock()
        device.configure = Mock()
        result = unconfigure_ip_arp_inspection_vlan_logging(device, '10,20', 'dhcp-bindings', None)
        self.assertIsNone(result)
        device.configure(['no ip arp inspection vlan logging dhcp-bindings 10,20'])