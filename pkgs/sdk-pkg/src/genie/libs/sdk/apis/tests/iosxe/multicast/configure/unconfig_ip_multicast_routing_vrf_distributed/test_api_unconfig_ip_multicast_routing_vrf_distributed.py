import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    unconfig_ip_multicast_routing_vrf_distributed,
)


class TestUnconfigIpMulticastRoutingVrfDistributed(TestCase):

    def test_unconfig_ip_multicast_routing_vrf_distributed(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfig_ip_multicast_routing_vrf_distributed(device, "20")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no ip multicast-routing vrf 20 distributed")


if __name__ == "__main__":
    unittest.main()
