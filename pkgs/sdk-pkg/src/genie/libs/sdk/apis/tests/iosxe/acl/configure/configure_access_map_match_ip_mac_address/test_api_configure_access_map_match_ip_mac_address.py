from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_map_match_ip_mac_address


class TestConfigureAccessMapMatchIpMacAddress(TestCase):

    def test_configure_access_map_match_ip_mac_address(self):
        self.device = Mock()
        configure_access_map_match_ip_mac_address(self.device, 'mymap', 'ip', '101', 'forward')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan access-map mymap', 'match ip address 101', 'action forward'],)
        )
