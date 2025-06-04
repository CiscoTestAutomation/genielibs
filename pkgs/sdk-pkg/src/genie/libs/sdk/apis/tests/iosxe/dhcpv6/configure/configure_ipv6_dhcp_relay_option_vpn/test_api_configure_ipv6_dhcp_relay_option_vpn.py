from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_option_vpn
from unittest.mock import Mock

class TestConfigureIpv6DhcpRelayOptionVpn(TestCase):

    def test_configure_ipv6_dhcp_relay_option_vpn(self):
        self.device = Mock()
        configure_ipv6_dhcp_relay_option_vpn(self.device, 'Vlan1500')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface Vlan1500', 'ipv6 dhcp relay option vpn'],))

