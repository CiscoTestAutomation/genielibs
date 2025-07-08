import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.arp.configure import configure_ip_arp_inspection_filter


class TestConfigureIpArpInspectionFilter(unittest.TestCase):

    def test_configure_ip_arp_inspection_filter(self):
        device = Mock()

        device.configure = Mock()

        result = configure_ip_arp_inspection_filter(
            device=device,
            arp_name='allowed_acl',
            vlan_id='10'
        )

        self.assertIsNone(result)

        device.configure.assert_called_once_with([
            'ip arp inspection filter allowed_acl vlan 10'
        ])