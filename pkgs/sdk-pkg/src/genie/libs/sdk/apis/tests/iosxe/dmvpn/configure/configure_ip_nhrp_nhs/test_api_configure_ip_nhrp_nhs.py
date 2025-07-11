from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_nhs
from unittest.mock import Mock

class TestConfigureIpNhrpNhs(TestCase):

    def test_configure_ip_nhrp_nhs(self):
        self.device = Mock()
        configure_ip_nhrp_nhs(self.device, 'tu0', '192.168.10.1')
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp nhs 192.168.10.1']))

