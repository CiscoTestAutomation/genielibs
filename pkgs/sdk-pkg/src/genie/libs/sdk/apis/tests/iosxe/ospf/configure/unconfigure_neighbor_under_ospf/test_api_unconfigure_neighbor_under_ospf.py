import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_neighbor_under_ospf,
)


class TestUnconfigureNeighborUnderOspf(TestCase):

    def test_unconfigure_neighbor_under_ospf(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_neighbor_under_ospf(device, 2, "55.55.55.2", 10)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "router ospf 2",
                "no neighbor 55.55.55.2 cost 10",
            ],
        )


if __name__ == "__main__":
    unittest.main()
