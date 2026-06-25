import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_physical_interface_vmi,
)


class TestConfigurePhysicalInterfaceVmi(TestCase):

    def test_configure_physical_interface_vmi(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_physical_interface_vmi(
            device,
            "vmi1",
            "GigabitEthernet1",
            "bypass",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vmi1", sent_commands)
        self.assertIn("physical-interface GigabitEthernet1", sent_commands)
        self.assertIn("mode bypass", sent_commands)

    def test_configure_physical_interface_vmi_without_mode(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_physical_interface_vmi(
            device,
            "vmi1",
            "GigabitEthernet1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface vmi1", sent_commands)
        self.assertIn("physical-interface GigabitEthernet1", sent_commands)


if __name__ == "__main__":
    unittest.main()