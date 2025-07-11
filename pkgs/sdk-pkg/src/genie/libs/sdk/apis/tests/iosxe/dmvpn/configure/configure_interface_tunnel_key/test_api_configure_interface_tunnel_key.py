from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_interface_tunnel_key
from unittest.mock import Mock

class TestConfigureInterfaceTunnelKey(TestCase):

    def test_configure_interface_tunnel_key(self):
        self.device = Mock()
        configure_interface_tunnel_key(self.device, 'tunnel1', 1234)
        self.device.configure.assert_called_with((['interface tunnel1', 'tunnel key 1234']))
        