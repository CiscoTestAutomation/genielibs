import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_vlan


class TestConfigureIpArpInspectionVlan(unittest.TestCase):

    def test_configure_ip_arp_inspection_vlan(self):
        device = Mock()
        device.configure = Mock()
        result = configure_ip_arp_inspection_vlan(device, 10)
        self.assertIsNone(result)
        device.configure.assert_called_once_with(['ip arp inspection vlan 10'])