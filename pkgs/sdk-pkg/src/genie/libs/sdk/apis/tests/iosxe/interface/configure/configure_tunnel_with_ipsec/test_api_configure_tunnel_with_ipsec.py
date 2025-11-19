from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_tunnel_with_ipsec
from unittest.mock import Mock


class TestConfigureTunnelWithIpsec(TestCase):

    def test_configure_tunnel_with_ipsec(self):
        self.device = Mock()
        result = configure_tunnel_with_ipsec(self.device, 'Tunnel1', 'ipv4', '1.1.1.1', '255.255.255.255', 'Te0/0/2', '17.17.17.2', None, None, '1::1', 128, 'gre', 'ipsec', 'IPSEC_PROFILE', None, None, None, 1, True, 'virtual-template 1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Tunnel1', 'ip address 1.1.1.1 255.255.255.255', 'ipv6 enable', 'ipv6 address 1::1/128', 'tunnel mode gre ip', 'tunnel source Te0/0/2', 'tunnel destination 17.17.17.2', 'tunnel protection ipsec profile IPSEC_PROFILE', 'ip nhrp network-id 1', 'ip nhrp redirect', 'ip nhrp shortcut virtual-template 1'],)
        )
