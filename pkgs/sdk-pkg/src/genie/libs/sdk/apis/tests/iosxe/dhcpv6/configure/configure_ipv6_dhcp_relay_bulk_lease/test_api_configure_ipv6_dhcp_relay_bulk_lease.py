from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_relay_bulk_lease
from unittest.mock import Mock


class TestConfigureIpv6DhcpRelayBulkLease(TestCase):

    def test_configure_ipv6_dhcp_relay_bulk_lease(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_relay_bulk_lease(self.device, 'retry', '5')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp-relay bulk-lease retry 5'],)
        )
