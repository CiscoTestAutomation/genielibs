import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.isis.configure import unconfig_interface_isis


class TestUnconfigInterfaceIsis(TestCase):

    def test_unconfig_interface_isis(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_interface_isis(
            device,
            "TwentyFiveGigE1/0/2",
            "False",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface TwentyFiveGigE1/0/2",
                "no ipv6 router isis",
            ],
        )


if __name__ == "__main__":
    unittest.main()
