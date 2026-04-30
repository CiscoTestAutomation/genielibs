from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.interface.configure import configure_interface_ipv6_nd


class TestConfigureInterfaceIpv6Nd(TestCase):

    def test_configure_interface_ipv6_nd_all_options(self):
        self.device = Mock()
        configure_interface_ipv6_nd(
            self.device, 'GigabitEthernet0/0',
            ns_interval=1782000, dad_attempts=0,
            ipv6_enable=True
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ipv6 enable",
                " ipv6 nd ns-interval 1782000",
                " ipv6 nd dad attempts 0",
                " no shutdown",
                " no keepalive",
            ]
        )

    def test_configure_interface_ipv6_nd_minimal(self):
        self.device = Mock()
        configure_interface_ipv6_nd(
            self.device, 'GigabitEthernet0/0',
            ns_interval=1782000
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " ipv6 nd ns-interval 1782000",
                " no shutdown",
                " no keepalive",
            ]
        )
