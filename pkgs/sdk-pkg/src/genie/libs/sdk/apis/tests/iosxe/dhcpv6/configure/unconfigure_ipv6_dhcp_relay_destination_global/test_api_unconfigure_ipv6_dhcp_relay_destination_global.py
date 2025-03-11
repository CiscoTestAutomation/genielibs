from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_destination_global
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpRelayDestinationGlobal(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_destination_global(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_relay_destination_global(self.device, 'GigabitEthernet1/0/1', '20::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'no ipv6 dhcp relay destination global 20::1'],)
        )
