import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mac.configure import (
    configure_default_mac_global_address_table_notification_change,
)


class TestConfigureDefaultMacGlobalAddressTableNotificationChange(TestCase):

    def test_configure_default_mac_global_address_table_notification_change(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_default_mac_global_address_table_notification_change(
            device,
            "history-size",
            None,
            None,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(
            sent_command,
            "default mac address-table notification change history-size",
        )


if __name__ == "__main__":
    unittest.main()
