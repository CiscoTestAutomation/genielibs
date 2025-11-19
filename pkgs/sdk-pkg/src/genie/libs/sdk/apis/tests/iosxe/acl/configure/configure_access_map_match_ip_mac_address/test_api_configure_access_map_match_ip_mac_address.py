from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_map_match_ip_mac_address
from unittest.mock import Mock


class TestConfigureAccessMapMatchIpMacAddress(TestCase):

    def test_configure_access_map_match_ip_mac_address(self):
        self.device = Mock()
        result = configure_access_map_match_ip_mac_address(self.device, 'mymap', 'ip', '101', 'forward', 'address')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vlan access-map mymap', 'match ip address 101', 'action forward'],)
        )
