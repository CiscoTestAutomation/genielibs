from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcpv6.configure import configure_ipv6_dhcp_route_add
from unittest.mock import Mock


class TestConfigureIpv6DhcpRouteAdd(TestCase):

    def test_configure_ipv6_dhcp_route_add(self):
        self.device = Mock()
        result = configure_ipv6_dhcp_route_add(self.device, 'iana-route-add')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ipv6 dhcp iana-route-add'],)
        )
