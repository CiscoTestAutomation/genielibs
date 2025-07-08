from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_map_multicast_dynamic
from unittest.mock import Mock

class TestConfigureIpNhrpMapMulticastDynamic(TestCase):

    def test_configure_ip_nhrp_map_multicast_dynamic(self):
        self.device = Mock()
        configure_ip_nhrp_map_multicast_dynamic(self.device, 'tu0')
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp map multicast dynamic']))
        
