from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.static_routing.configure import configure_ipv6_static_route


class TestConfigureIpv6StaticRoute(TestCase):

    def test_configure_ipv6_static_route(self):
        self.device = Mock()
        configure_ipv6_static_route(
            self.device, '2001:db8:2::', '64', '2001:db8:1::1'
        )
        self.device.configure.assert_called_once_with(
            "ipv6 route 2001:db8:2::/64 2001:db8:1::1"
        )
