import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import shutdown_interface_range


class TestShutdownInterfaceRange(TestCase):

    def test_shutdown_interface_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = shutdown_interface_range(
            device,
            "vlan",
            2,
            513,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface range vlan 2 - 513",
                "shut",
            ],
        )


if __name__ == "__main__":
    unittest.main()