from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_destination_global
from unittest.mock import Mock


class TestConfigureIpv6DhcpRelayDestinationGlobal(TestCase):

    def test_configure_ipv6_dhcp_relay_destination_global(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_relay_destination_global(self.device, 'GigabitEthernet1/0/1', '20::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/0/1', 'ipv6 dhcp relay destination global 20::1'],)
        )
