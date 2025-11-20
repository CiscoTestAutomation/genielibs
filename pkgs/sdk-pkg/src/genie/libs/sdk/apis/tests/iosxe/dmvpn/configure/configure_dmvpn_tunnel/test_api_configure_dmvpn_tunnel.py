from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_dmvpn_tunnel
from unittest.mock import Mock


class TestConfigureDmvpnTunnel(TestCase):

    def test_configure_dmvpn_tunnel(self):
        self.device = Mock()
        result = configure_dmvpn_tunnel(self.device, 'Tunnel2', None, None, None, None, 'ipv4', None, None, None, None, None, None, None, False, None, False, None, None, None, True, None, None, None, None, None, None, None, None, False, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Tunnel2', 'ip nhrp redirect'],)
        )
