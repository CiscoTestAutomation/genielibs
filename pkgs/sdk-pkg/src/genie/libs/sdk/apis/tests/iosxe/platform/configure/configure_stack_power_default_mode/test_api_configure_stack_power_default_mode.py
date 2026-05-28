import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stack_power_default_mode


class TestConfigureStackPowerDefaultMode(unittest.TestCase):

    def test_configure_stack_power_default_mode(self):
        device = Mock()

        result = configure_stack_power_default_mode(device, 'test')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack test', 'default mode'],)
        )