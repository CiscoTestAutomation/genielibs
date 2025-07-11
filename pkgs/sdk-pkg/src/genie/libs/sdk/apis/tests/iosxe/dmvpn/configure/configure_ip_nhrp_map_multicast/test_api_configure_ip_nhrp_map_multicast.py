from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_map_multicast
from unittest.mock import Mock

class TestConfigureIpNhrpMapMulticast(TestCase):

    def test_configure_ip_nhrp_map_multicast(self):
        self.device = Mock()
        configure_ip_nhrp_map_multicast(self.device, 'tu0', '2.2.2.2')
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp map multicast 2.2.2.2']))
