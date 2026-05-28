import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_power_inline_auto_max


class TestConfigurePowerInlineAutoMax(unittest.TestCase):

    def test_configure_power_inline_auto_max(self):
        device = Mock()

        result = configure_power_inline_auto_max(device, 'te2/0/1', '10000')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te2/0/1', 'power inline auto max 10000'],)
        )