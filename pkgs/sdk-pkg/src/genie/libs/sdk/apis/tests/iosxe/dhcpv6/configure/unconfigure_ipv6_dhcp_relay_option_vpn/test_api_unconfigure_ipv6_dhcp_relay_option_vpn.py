from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_option_vpn
from unittest.mock import Mock

class TestUnconfigureIpv6DhcpRelayOptionVpn(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_option_vpn(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_relay_option_vpn(self.device, 'Vlan1500')
        self.device.configure.assert_called_with(['interface Vlan1500', 'no ipv6 dhcp relay option vpn'])