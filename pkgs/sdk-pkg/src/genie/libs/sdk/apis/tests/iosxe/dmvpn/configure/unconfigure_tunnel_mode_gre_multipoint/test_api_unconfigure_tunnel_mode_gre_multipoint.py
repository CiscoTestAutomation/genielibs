from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_tunnel_mode_gre_multipoint
from unittest.mock import Mock

class TestUnconfigureTunnelModeGreMultipoint(TestCase):

    def test_unconfigure_tunnel_mode_gre_multipoint(self):
        self.device = Mock()
        unconfigure_tunnel_mode_gre_multipoint(self.device, 'tu0')
        self.device.configure.assert_called_with(['interface tu0', 'no tunnel mode gre multipoint'])
