from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_relay_bulk_lease
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpRelayBulkLease(TestCase):

    def test_unconfigure_ipv6_dhcp_relay_bulk_lease(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_relay_bulk_lease(self.device, 'retry', '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp-relay bulk-lease retry 5'],)
        )
