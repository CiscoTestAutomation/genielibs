from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_default_stack_power_switch_power_priority


class TestConfigureDefaultStackPowerSwitchPowerPriority(TestCase):

    def test_configure_default_stack_power_switch_power_priority(self):
        device = Mock()
        result = configure_default_stack_power_switch_power_priority(
            device,
            'switch',
            1,
            'high',
            13
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power switch 1', 'default power-priority high 13'],)
        )