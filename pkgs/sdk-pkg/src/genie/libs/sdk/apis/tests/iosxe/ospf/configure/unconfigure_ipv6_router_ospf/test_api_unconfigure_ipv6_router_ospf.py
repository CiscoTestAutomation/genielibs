import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ipv6_router_ospf,
)


class TestUnconfigureIpv6RouterOspf(TestCase):

    def test_unconfigure_ipv6_router_ospf(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_router_ospf(device, 10)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no ipv6 router ospf 10")


if __name__ == "__main__":
    unittest.main()
