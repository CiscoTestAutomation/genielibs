from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_map
from unittest.mock import Mock

class TestUnconfigureIpNhrpMap(TestCase):

    def test_unconfigure_ip_nhrp_map(self):
        self.device = Mock()
        unconfigure_ip_nhrp_map(self.device, 'tu0', '192.162.10.1', '1.1.1.1')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp map 192.162.10.1 1.1.1.1'])