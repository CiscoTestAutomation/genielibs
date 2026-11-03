import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ipv6_ospf_routing_on_interface,
)


class TestUnconfigureIpv6OspfRoutingOnInterface(TestCase):

    def test_unconfigure_ipv6_ospf_routing_on_interface(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_ospf_routing_on_interface(
            device,
            "HundredGigE1/0/21",
            "1",
            0,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface HundredGigE1/0/21",
                "no ipv6 ospf 1 area 0",
            ],
        )


if __name__ == "__main__":
    unittest.main()
