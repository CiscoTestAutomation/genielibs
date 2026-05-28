import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import (
    configure_console_default_privilege_level,
)


class TestConfigureConsoleDefaultPrivilegeLevel(TestCase):

    def test_configure_console_default_privilege_level(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_console_default_privilege_level(device, "10")

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertIn("line console 0", sent_commands)
        self.assertIn("privilege level 10", sent_commands)


if __name__ == "__main__":
    unittest.main()