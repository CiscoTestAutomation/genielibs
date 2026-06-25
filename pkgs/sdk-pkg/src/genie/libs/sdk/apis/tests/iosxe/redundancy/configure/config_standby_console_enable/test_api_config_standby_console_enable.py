import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.redundancy.configure import (
    config_standby_console_enable
)


class TestConfigStandbyConsoleEnable(unittest.TestCase):

    def test_config_standby_console_enable(self):
        device = Mock()

        result = config_standby_console_enable(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['redundancy', 'main-cpu', 'standby console enable'],)
        )