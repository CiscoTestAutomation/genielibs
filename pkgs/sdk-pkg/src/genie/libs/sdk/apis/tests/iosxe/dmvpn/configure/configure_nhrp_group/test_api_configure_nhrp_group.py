from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_nhrp_group
from unittest.mock import Mock

class TestConfigureNhrpGroup(TestCase):

    def test_configure_nhrp_group(self):
        self.device = Mock()
        configure_nhrp_group(self.device, 'tu0', 's1')
        self.device.configure.assert_called_with((['interface tu0', 'nhrp group s1']))