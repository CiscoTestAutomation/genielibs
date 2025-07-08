from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_authentication
from unittest.mock import Mock

class TestUnconfigureIpNhrpAuthentication(TestCase):
    def test_unconfigure_ip_nhrp_authentication(self):
        self.device = Mock()
        unconfigure_ip_nhrp_authentication(self.device, 'tu0', 'testing')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp authentication testing'])
