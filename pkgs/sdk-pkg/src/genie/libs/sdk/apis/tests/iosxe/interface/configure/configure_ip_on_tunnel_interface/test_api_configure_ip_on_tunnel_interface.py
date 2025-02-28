from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_tunnel_interface
from unittest.mock import Mock


class TestConfigureIpOnTunnelInterface(TestCase):

    def test_configure_ip_on_tunnel_interface(self):
        self.device = Mock()
        result = configure_ip_on_tunnel_interface(self.device, 'Tunnel10', '41.1.1.1', '255.255.255.0', '42.1.1.1', '42.1.1.2', 10, None, None, None, 'gre', None, None, None, None, None, None, 'ip')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Tunnel10', 'ip address 41.1.1.1 255.255.255.0', 'tunnel mode gre ip', 'tunnel source 42.1.1.1', 'tunnel destination 42.1.1.2', 'keepalive 10'],)
        )
