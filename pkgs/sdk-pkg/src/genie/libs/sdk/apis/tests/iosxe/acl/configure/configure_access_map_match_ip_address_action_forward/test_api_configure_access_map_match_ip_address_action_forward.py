from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import configure_access_map_match_ip_address_action_forward
from unittest.mock import Mock

class TestConfigureAccessMapMatchIpAddressActionForward(TestCase):

    def test_configure_access_map_match_ip_address_action_forward(self):
        self.device = Mock()
        configure_access_map_match_ip_address_action_forward(self.device, 'ana')
        self.device.configure.assert_called_with(['vlan access-map ana', 'match ip address ana', 'action forward', 'exit'])
