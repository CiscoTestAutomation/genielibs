import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_route_map,
)


class TestUnconfigureRouteMap(TestCase):

    def test_unconfigure_route_map(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_route_map(device, "rm_v4pbr_nexthop1", None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "no route-map rm_v4pbr_nexthop1")


if __name__ == "__main__":
    unittest.main()
