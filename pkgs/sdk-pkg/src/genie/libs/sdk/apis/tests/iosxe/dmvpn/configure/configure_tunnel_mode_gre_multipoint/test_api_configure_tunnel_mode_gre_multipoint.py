from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_tunnel_mode_gre_multipoint
from unittest.mock import Mock

class TestConfigureTunnelModeGreMultipoint(TestCase):

    def test_configure_tunnel_mode_gre_multipoint(self):
        self.device = Mock()
        configure_tunnel_mode_gre_multipoint(self.device, 'tu0')
        self.device.configure.assert_called_with(['interface tu0', 'tunnel mode gre multipoint'])
        
