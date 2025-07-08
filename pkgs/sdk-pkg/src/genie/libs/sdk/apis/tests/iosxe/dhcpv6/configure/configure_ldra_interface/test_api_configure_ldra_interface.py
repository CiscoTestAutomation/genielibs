from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ldra_interface
from unittest.mock import Mock

class TestConfigureLdraInterface(TestCase):

    def test_configure_ldra_interface(self):
        self.device = Mock()
        configure_ldra_interface(self.device, 'TwentyFiveGigE1/0/1', None, 'server-facing', None)
        self.device.configure.assert_called_with(['interface TwentyFiveGigE1/0/1', 'ipv6 dhcp-ldra attach-policy server-facing'])

