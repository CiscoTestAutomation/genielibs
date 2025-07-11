import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_vlan_logging


class TestConfigureIpArpInspectionVlanLogging(unittest.TestCase):

    def test_configure_ip_arp_inspection_vlan_logging(self):
        device = Mock()
        device.configure = Mock()
        result = configure_ip_arp_inspection_vlan_logging(device, '10,20', 'acl-match', None)
        self.assertIsNone(result)
        device.configure(['ip arp inspection vlan logging acl-match 10,20'])