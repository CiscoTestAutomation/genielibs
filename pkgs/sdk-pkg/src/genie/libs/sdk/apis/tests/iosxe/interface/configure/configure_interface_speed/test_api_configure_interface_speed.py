import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_speed


class TestConfigureInterfaceSpeed(TestCase):

    def test_configure_interface_speed(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_speed(
            device,
            "GigabitEthernet1/2",
            "10",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/2", sent_commands)
        self.assertIn("speed 10", sent_commands)


if __name__ == "__main__":
    unittest.main()