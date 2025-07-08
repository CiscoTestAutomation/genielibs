from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_nhrp_group
from unittest.mock import Mock

class TestUnconfigureNhrpGroup(TestCase):

    def test_unconfigure_nhrp_group(self):
        self.device = Mock()
        unconfigure_nhrp_group(self.device, 'tu0', 's1')
        self.device.configure.assert_called_with(['interface tu0', 'no nhrp group s1'])
