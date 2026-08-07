import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    unconfigure_interface_storm_control_level,
)


class TestUnconfigureInterfaceStormControlLevel(TestCase):

    def test_unconfigure_interface_storm_control_level(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "unicast",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet1/0/2",
            sent_commands,
        )
        self.assertIn(
            "no storm-control unicast level",
            sent_commands,
        )

    def test_unconfigure_interface_storm_control_level_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "broadcast",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet1/0/2",
            sent_commands,
        )
        self.assertIn(
            "no storm-control broadcast level",
            sent_commands,
        )

    def test_unconfigure_interface_storm_control_level_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "multicast",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn(
            "interface GigabitEthernet1/0/2",
            sent_commands,
        )
        self.assertIn(
            "no storm-control multicast level",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()