from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_destination_ipv6address
from unittest.mock import Mock

class TestConfigureIpv6DhcpRelayDestinationIpv6address(TestCase):

    def test_configure_ipv6_dhcp_relay_destination_ipv6address(self):
        self.device = Mock()
        configure_ipv6_dhcp_relay_destination_ipv6address(self.device, 'Vlan1500', '2000::1')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['interface Vlan1500', 'ipv6 dhcp relay destination 2000::1'],))
        