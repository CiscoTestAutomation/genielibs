import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_line_vty


class TestConfigureLineVty(unittest.TestCase):

    def test_configure_line_vty(self):
        device = Mock()

        result = configure_line_vty(device, '1', '2')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('line vty 1 2',)
        )