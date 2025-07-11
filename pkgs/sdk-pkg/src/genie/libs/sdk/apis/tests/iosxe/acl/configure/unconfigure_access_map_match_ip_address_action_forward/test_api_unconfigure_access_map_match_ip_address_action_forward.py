from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_access_map_match_ip_address_action_forward


class TestUnconfigureAccessMapMatchIpAddressActionForward(TestCase):

    def test_unconfigure_access_map_match_ip_address_action_forward(self):
        self.device = Mock()
        unconfigure_access_map_match_ip_address_action_forward(self.device, 'vacl1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no vlan access-map vacl1' ,)
        )
