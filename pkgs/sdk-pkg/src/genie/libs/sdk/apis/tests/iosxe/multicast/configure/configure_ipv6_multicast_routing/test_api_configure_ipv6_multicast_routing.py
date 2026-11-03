import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_multicast_routing,
)


class TestConfigureIpv6MulticastRouting(TestCase):

    def test_configure_ipv6_multicast_routing(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_multicast_routing(device, None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ipv6 multicast-routing")

    def test_configure_ipv6_multicast_routing_1(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_multicast_routing(device, "green")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ipv6 multicast-routing vrf green")


if __name__ == "__main__":
    unittest.main()
