import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import shutdown_sub_interface_range


class TestShutdownSubInterfaceRange(TestCase):

    def test_shutdown_sub_interface_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = shutdown_sub_interface_range(
            device,
            "GigabitEthernet5/0/33",
            2,
            129,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface range GigabitEthernet5/0/33.2 - GigabitEthernet5/0/33.129",
                "shut",
            ],
        )


if __name__ == "__main__":
    unittest.main()