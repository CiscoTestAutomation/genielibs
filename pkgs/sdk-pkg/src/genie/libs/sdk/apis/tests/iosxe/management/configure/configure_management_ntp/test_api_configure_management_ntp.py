import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_ntp,
)


class TestConfigureManagementNtp(TestCase):

    def test_configure_management_ntp(self):
        device = Mock()
        device.state_machine.current_state = "enable"

        device.testbed.servers = {
            "ntp": {
                "address": "127.0.0.1",
            },
        }
        device.management = {}

        device.configure.return_value = "ntp server 127.0.0.1\r\n"

        result = configure_management_ntp(device)

        self.assertEqual(
            result,
            "ntp server 127.0.0.1\r\n",
        )

        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ntp server 127.0.0.1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
