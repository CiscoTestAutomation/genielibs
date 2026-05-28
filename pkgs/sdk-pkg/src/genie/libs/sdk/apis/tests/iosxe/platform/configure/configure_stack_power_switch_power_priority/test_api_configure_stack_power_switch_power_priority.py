import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stack_power_switch_power_priority


class TestConfigureStackPowerSwitchPowerPriority(unittest.TestCase):

    def test_configure_stack_power_switch_power_priority(self):
        device = Mock()

        result = configure_stack_power_switch_power_priority(device, 1, 'high', 4, True)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power switch 1', 'default power-priority high'],)
        )