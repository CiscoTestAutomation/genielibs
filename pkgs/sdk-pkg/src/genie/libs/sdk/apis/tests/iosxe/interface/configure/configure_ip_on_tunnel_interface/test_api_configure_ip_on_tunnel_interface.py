from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_tunnel_interface
from unittest.mock import Mock


class TestConfigureIpOnTunnelInterface(TestCase):

    def test_configure_ip_on_tunnel_interface(self):
        self.device = Mock()
        result = configure_ip_on_tunnel_interface(self.device, 'Tunnel10', None, None, '10.10.10.1', '20.1.11.1', 10, None, None, None, None, None, None, None, None, None, None, 'ipv4', '200', True, 'min-mtu 512')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Tunnel10', 'tunnel source 10.10.10.1', 'tunnel destination 20.1.11.1', 'keepalive 10', 'tunnel key 200', 'tunnel path-mtu-discovery min-mtu 512'],)
        )
