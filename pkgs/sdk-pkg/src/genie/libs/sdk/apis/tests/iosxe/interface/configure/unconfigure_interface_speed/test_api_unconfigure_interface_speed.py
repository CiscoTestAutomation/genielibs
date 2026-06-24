import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_speed


class TestUnconfigureInterfaceSpeed(TestCase):

    def test_unconfigure_interface_speed(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_speed(
            device,
            "Gig0",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Gig0",
                "no speed",
            ],
        )


if __name__ == "__main__":
    unittest.main()