import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_stack_power_switch_no_standalone


class TestConfigureStackPowerSwitchNoStandalone(unittest.TestCase):

    def test_configure_stack_power_switch_no_standalone(self):
        device = Mock()

        result = configure_stack_power_switch_no_standalone(device, 1)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['stack-power switch 1', 'no standalone'],)
        )