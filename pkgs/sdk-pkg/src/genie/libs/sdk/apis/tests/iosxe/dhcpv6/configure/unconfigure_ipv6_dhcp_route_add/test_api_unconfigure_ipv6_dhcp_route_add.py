from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import unconfigure_ipv6_dhcp_route_add
from unittest.mock import Mock


class TestUnconfigureIpv6DhcpRouteAdd(TestCase):

    def test_unconfigure_ipv6_dhcp_route_add(self):
        self.device = Mock()
        result = unconfigure_ipv6_dhcp_route_add(self.device, 'iana-route-add')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no ipv6 dhcp iana-route-add'],)
        )
