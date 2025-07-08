from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_network_id
from unittest.mock import Mock

class TestConfigureIpNhrpNetworkId(TestCase):

    def test_configure_ip_nhrp_network_id(self):
        self.device = Mock()
        configure_ip_nhrp_network_id(self.device, 'tu0', 1)
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp network-id 1']))
