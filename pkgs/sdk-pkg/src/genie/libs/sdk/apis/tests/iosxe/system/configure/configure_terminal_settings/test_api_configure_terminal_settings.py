from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.system.configure import (
    configure_terminal_settings,
)


class TestConfigureTerminalSettings(TestCase):

    def test_configure_terminal_settings(self):
        device = Mock()

        result = configure_terminal_settings(device, 20, 80)

        self.assertIsNone(result)
        device.execute.assert_called_once_with(
            ['terminal length 20', 'terminal width 80']
        )
