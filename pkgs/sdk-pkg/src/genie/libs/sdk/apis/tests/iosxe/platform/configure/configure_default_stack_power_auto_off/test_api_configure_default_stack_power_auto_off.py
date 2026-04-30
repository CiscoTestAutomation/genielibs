from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_default_stack_power_auto_off


class TestConfigureDefaultStackPowerAutoOff(TestCase):

    def test_configure_default_stack_power_auto_off(self):
        device = Mock()
        result = configure_default_stack_power_auto_off(
            device,
            'Powerstack-2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power stack Powerstack-2', 'default auto-off'],)
        )