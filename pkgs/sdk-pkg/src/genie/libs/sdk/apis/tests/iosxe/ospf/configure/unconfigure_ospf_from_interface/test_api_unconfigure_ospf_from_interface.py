import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ospf.configure import (
    unconfigure_ospf_from_interface,
)


class TestUnconfigureOspfFromInterface(TestCase):

    def test_unconfigure_ospf_from_interface(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ospf_from_interface(device, "loopback1", "1", "0")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface loopback1",
                "no ip ospf 1 area 0",
            ],
        )


if __name__ == "__main__":
    unittest.main()
