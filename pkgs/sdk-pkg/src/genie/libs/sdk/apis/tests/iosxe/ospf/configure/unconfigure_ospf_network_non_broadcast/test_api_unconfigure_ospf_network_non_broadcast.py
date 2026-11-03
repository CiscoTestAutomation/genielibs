import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospf_network_non_broadcast,
)


class TestUnconfigureOspfNetworkNonBroadcast(TestCase):

    def test_unconfigure_ospf_network_non_broadcast(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospf_network_non_broadcast(device, "tunnel1")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface tunnel1",
                "no ip ospf network non-broadcast",
            ],
        )


if __name__ == "__main__":
    unittest.main()
