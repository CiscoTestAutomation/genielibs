from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_nhs
from unittest.mock import Mock

class TestUnconfigureIpNhrpNhs(TestCase):
    
    def test_unconfigure_ip_nhrp_nhs(self):
        self.device = Mock()
        unconfigure_ip_nhrp_nhs(self.device, 'tu0', '192.168.10.1')
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp nhs 192.168.10.1'])
