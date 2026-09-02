import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_vty_lines,
)


class TestConfigureManagementVtyLines(TestCase):

    def test_configure_management_vty_lines(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.credentials = {
            "None": {
                "username": "admin",
                "password": "admin",
            },
        }

        device.execute.return_value = (
            "line vty 0 4\r\n"
            " exec-timeout 0 0\r\n"
            " login\r\n"
            " transport input telnet ssh\r\n"
            "line vty 5 15\r\n"
            " login\r\n"
            " transport input telnet ssh"
        )
        device.configure.return_value = None

        result = configure_management_vty_lines(
            device,
            "None",
            "telnet",
            False,
        )

        self.assertIsNone(result)

        device.execute.assert_called_once_with(
            "show running-config | section line vty"
        )

        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "line vty 0 15",
                "login local",
                "transport input telnet ssh",
            ],
        )


if __name__ == "__main__":
    unittest.main()
