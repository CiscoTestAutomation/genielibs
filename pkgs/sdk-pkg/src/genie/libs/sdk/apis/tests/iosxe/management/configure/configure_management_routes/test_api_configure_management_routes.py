import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_routes,
)


class TestConfigureManagementRoutes(TestCase):

    def test_configure_management_routes(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.management = {}

        result = configure_management_routes(device)

        self.assertIsNone(result)
        device.configure.assert_not_called()

    def test_configure_ipv4_and_ipv6_management_routes(self):
        device = Mock()
        device.management = {}
        routes = {
            "ipv4": [{
                "subnet": "198.51.100.0 255.255.255.0",
                "next_hop": "192.0.2.1",
            }],
            "ipv6": [{
                "subnet": "2001:db8:1::/64",
                "next_hop": "2001:db8::1",
            }],
        }

        configure_management_routes(device, routes=routes)

        device.configure.assert_called_once_with([
            "ip route 198.51.100.0 255.255.255.0 192.0.2.1",
            "ipv6 route 2001:db8:1::/64 2001:db8::1",
        ])

    def test_configure_ipv4_and_ipv6_management_routes_in_vrf(self):
        device = Mock()
        device.management = {}
        routes = {
            "ipv4": [{
                "subnet": "198.51.100.0 255.255.255.0",
                "next_hop": "192.0.2.1",
            }],
            "ipv6": [{
                "subnet": "2001:db8:1::/64",
                "next_hop": "2001:db8::1",
            }],
        }

        configure_management_routes(device, routes=routes, vrf="Mgmt-vrf")

        device.configure.assert_called_once_with([
            "ip route vrf Mgmt-vrf 198.51.100.0 255.255.255.0 192.0.2.1",
            "ipv6 route vrf Mgmt-vrf 2001:db8:1::/64 2001:db8::1",
        ])


if __name__ == "__main__":
    unittest.main()
