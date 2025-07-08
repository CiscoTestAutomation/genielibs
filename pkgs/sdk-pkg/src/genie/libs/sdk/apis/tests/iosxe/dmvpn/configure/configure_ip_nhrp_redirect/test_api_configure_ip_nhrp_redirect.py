from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_redirect
from unittest.mock import Mock

class TestConfigureIpNhrpRedirect(TestCase):

    def test_configure_ip_nhrp_redirect(self):
        self.device = Mock()
        result = configure_ip_nhrp_redirect(self.device, 'tu0')
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp redirect']))
