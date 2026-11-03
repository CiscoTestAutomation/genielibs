import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospfv3_network,
)


class TestUnconfigureOspfv3Network(TestCase):

    def test_unconfigure_ospfv3_network(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospfv3_network(
            device=device,
            interface="HundredGigE1/0/21",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface HundredGigE1/0/21",
                "no ipv6 ospf network",
            ],
        )


if __name__ == "__main__":
    unittest.main()
