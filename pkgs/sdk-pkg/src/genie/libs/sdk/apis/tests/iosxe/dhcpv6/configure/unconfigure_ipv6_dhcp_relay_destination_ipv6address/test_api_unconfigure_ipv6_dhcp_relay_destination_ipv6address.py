from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_destination_ipv6address
from unittest.mock import Mock

class TestUnconfigureIpv6DhcpRelayDestinationIpv6address(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_destination_ipv6address(self):
        self.device = Mock()
        unconfigure_ipv6_dhcp_relay_destination_ipv6address(self.device, 'Vlan1500', '2000::1')
        self.device.configure.assert_called_with(['interface Vlan1500', 'no ipv6 dhcp relay destination 2000::1'])
       
