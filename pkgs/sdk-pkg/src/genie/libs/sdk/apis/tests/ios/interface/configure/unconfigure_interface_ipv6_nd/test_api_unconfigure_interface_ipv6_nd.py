from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.ios.interface.configure import unconfigure_interface_ipv6_nd


class TestUnconfigureInterfaceIpv6Nd(TestCase):

    def test_unconfigure_interface_ipv6_nd(self):
        self.device = Mock()
        unconfigure_interface_ipv6_nd(
            self.device, 'GigabitEthernet0/0',
            ns_interval=1782000, dad_attempts=0,
            ipv6_enable=True
        )
        self.device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet0/0",
                " no ipv6 enable",
                " no ipv6 nd ns-interval 1782000",
                " no ipv6 nd dad attempts 0",
                " shutdown",
                " keepalive",
            ]
        )
