import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_management_telnet,
)


class TestConfigureManagementTelnet(TestCase):

    def test_configure_management_telnet(self):
        device = Mock()
        device.state_machine.current_state = "enable"

        device.api.configure_management_credentials = Mock()
        device.api.configure_management_vty_lines = Mock()

        result = configure_management_telnet(device)

        self.assertIsNone(result)

        device.api.configure_management_credentials.assert_called_once_with(
            "default",
            username=None,
            password=None,
        )

        device.api.configure_management_vty_lines.assert_called_once_with(
            authentication="default",
            transport="telnet",
        )


if __name__ == "__main__":
    unittest.main()
