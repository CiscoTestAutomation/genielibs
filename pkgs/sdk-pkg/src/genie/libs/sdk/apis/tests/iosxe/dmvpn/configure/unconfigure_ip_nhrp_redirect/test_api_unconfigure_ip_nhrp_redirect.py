from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_redirect
from unittest.mock import Mock
class TestUnconfigureIpNhrpRedirect(TestCase):

    def test_unconfigure_ip_nhrp_redirect(self):
        self.device = Mock()
        unconfigure_ip_nhrp_redirect(self.device, 'tu0')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp redirect'])