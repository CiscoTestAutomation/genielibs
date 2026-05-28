import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_interface_authentication_violation,
)


class TestConfigureInterfaceAuthenticationViolation(TestCase):

    def test_configure_interface_authentication_violation(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_authentication_violation(
            device,
            "Gi1/0/3",
            "shutdown",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Gi1/0/3", sent_commands)
        self.assertIn("authentication violation shutdown", sent_commands)

    def test_configure_interface_authentication_violation_1(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_interface_authentication_violation(
            device,
            "Gi1/0/3",
            "protect",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("interface Gi1/0/3", sent_commands)
        self.assertIn("authentication violation protect", sent_commands)


if __name__ == "__main__":
    unittest.main()