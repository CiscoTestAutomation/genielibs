from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_authentication
from unittest.mock import Mock

class TestConfigureIpNhrpAuthentication(TestCase):

    def test_configure_ip_nhrp_authentication(self):
        self.device = Mock()
        configure_ip_nhrp_authentication(self.device, 'tu0', 'testing')
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp authentication testing']))

