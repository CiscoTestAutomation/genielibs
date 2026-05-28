import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stack_power_mode_power_shared


class TestConfigureStackPowerModePowerShared(unittest.TestCase):

    def test_configure_stack_power_mode_power_shared(self):
        device = Mock()

        result = configure_stack_power_mode_power_shared(device, 'Powerstack-Ring', None)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack Powerstack-Ring', 'mode power-shared'],)
        )