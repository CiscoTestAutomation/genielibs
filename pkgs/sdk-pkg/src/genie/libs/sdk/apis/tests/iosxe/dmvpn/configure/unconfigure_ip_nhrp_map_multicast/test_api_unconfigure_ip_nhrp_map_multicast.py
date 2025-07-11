from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_map_multicast
from unittest.mock import Mock

class TestUnconfigureIpNhrpMapMulticast(TestCase):

    def test_unconfigure_ip_nhrp_map_multicast(self):
        self.device = Mock()
        unconfigure_ip_nhrp_map_multicast(self.device, 'tu0', '2.2.2.2')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp map multicast 2.2.2.2'])



