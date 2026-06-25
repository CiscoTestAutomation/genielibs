import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_storm_control_level


class TestConfigureInterfaceStormControlLevel(TestCase):

    def test_configure_interface_storm_control_level(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "unicast",
            7,
            "",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control unicast level 7", sent_commands)

    def test_configure_interface_storm_control_level_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "broadcast",
            7,
            4,
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control broadcast level 7 4", sent_commands)

    def test_configure_interface_storm_control_level_2(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "multicast",
            1000,
            990,
            "pps",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control multicast level pps 1000 990", sent_commands)

    def test_configure_interface_storm_control_level_3(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_storm_control_level(
            device,
            "GigabitEthernet1/0/2",
            "unicast",
            10000,
            9990,
            "bps",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface GigabitEthernet1/0/2", sent_commands)
        self.assertIn("storm-control unicast level bps 10000 9990", sent_commands)


if __name__ == "__main__":
    unittest.main()