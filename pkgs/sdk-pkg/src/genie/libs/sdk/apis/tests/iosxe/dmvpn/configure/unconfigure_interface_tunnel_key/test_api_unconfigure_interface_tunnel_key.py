from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import unconfigure_interface_tunnel_key
from unittest.mock import Mock

class TestUnconfigureInterfaceTunnelKey(TestCase):

    def test_unconfigure_interface_tunnel_key(self):
        self.device = Mock()
        unconfigure_interface_tunnel_key(self.device, 'tunnel1')
        self.device.configure.assert_called_with(['interface tunnel1', 'no tunnel key'])
