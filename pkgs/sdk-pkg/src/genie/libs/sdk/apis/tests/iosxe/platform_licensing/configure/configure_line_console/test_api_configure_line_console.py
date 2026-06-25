import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform_licensing.configure import configure_line_console


class TestConfigureLineConsole(unittest.TestCase):

    def test_configure_line_console(self):
        device = Mock()

        result = configure_line_console(
            device,
            '0'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('line console 0',)
        )