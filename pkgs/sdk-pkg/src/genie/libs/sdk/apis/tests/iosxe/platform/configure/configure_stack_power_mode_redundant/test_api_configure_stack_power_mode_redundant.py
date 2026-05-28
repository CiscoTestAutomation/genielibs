import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stack_power_mode_redundant


class TestConfigureStackPowerModeRedundant(unittest.TestCase):

    def test_configure_stack_power_mode_redundant(self):
        device = Mock()

        result = configure_stack_power_mode_redundant(device, 'test', None)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack test', 'mode redundant'],)
        )