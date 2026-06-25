import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_storm_control_action


class TestConfigureInterfaceStormControlAction(TestCase):

    def test_configure_interface_storm_control_action(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_action(
            device,
            "GigabitEthernet1/0/2",
            "shutdown",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control action shutdown", sent_commands)

    def test_configure_interface_storm_control_action_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_action(
            device,
            "GigabitEthernet1/0/2",
            "trap",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control action trap", sent_commands)


if __name__ == "__main__":
    unittest.main()