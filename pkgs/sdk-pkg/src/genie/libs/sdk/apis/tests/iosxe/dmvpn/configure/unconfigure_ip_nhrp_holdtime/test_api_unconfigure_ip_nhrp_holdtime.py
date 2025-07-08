from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_ip_nhrp_holdtime
from unittest.mock import Mock

class TestUnconfigureIpNhrpHoldtime(TestCase):

    def test_unconfigure_ip_nhrp_holdtime(self):
        self.device = Mock()
        unconfigure_ip_nhrp_holdtime(self.device, 'tu0', 300)
        self.device.configure.assert_called_with(['interface tu0', 'no ip nhrp holdtime 300'])
