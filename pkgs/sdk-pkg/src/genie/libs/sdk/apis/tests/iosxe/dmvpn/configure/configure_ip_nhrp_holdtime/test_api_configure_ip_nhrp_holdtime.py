from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_ip_nhrp_holdtime
from unittest.mock import Mock

class TestConfigureIpNhrpHoldtime(TestCase):

    def test_configure_ip_nhrp_holdtime(self):
        self.device = Mock()
        configure_ip_nhrp_holdtime(self.device, 'tu0', 300)
        self.device.configure.assert_called_with((['interface tu0', 'ip nhrp holdtime 300']))
        
