from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_map_multicast_dynamic
from unittest.mock import Mock

class TestUnconfigureIpNhrpMapMulticastDynamic(TestCase):
    
    def test_unconfigure_ip_nhrp_map_multicast_dynamic(self):
        self.device = Mock()
        unconfigure_ip_nhrp_map_multicast_dynamic(self.device, 'tu0')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp map multicast dynamic'])
