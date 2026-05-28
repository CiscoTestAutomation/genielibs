from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.static_routing.configure import configure_static_route


class TestConfigureStaticRoute(TestCase):

    def test_configure_static_route(self):
        self.device = Mock()
        configure_static_route(
            self.device, '10.2.0.0', '255.255.255.0', '10.1.1.1'
        )
        self.device.configure.assert_called_once_with(
            "ip route 10.2.0.0 255.255.255.0 10.1.1.1"
        )
