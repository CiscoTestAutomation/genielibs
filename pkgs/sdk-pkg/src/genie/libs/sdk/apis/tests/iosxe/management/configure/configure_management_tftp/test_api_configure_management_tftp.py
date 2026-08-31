import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_tftp,
)


class TestConfigureManagementTftp(TestCase):

    def test_configure_management_tftp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.management = {
            "interface": "GigabitEthernet0",
        }
        device.configure.return_value = None

        result = configure_management_tftp(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ip tftp source-interface GigabitEthernet0",
            ],
        )


if __name__ == "__main__":
    unittest.main()
