from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_network_id
from unittest.mock import Mock

class TestUnconfigureIpNhrpNetworkId(TestCase):

    def test_unconfigure_ip_nhrp_network_id(self):
        self.device = Mock()
        unconfigure_ip_nhrp_network_id(self.device, 'tu0', 1)
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp network-id 1'])
        
