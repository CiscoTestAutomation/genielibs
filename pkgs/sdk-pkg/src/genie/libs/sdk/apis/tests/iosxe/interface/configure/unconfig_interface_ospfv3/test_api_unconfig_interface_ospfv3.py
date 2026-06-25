import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfig_interface_ospfv3


class TestUnconfigInterfaceOspfv3(TestCase):

    def test_unconfig_interface_ospfv3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_ospfv3(
            device,
            "vmi1",
            "1",
            0,
            False,
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface vmi1",
                "no ospfv3 1 ipv6 area 0",
                "no ospfv3 1 network manet",
            ],
        )


if __name__ == "__main__":
    unittest.main()