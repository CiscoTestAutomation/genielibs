import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_module_switch_number_auto_off_led


class TestUnconfigureHwModuleSwitchNumberAutoOffLed(unittest.TestCase):

    def test_unconfigure_hw_module_switch_number_auto_off_led(self):
        device = Mock()

        result = unconfigure_hw_module_switch_number_auto_off_led(device, '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no hw-module switch 1 auto-off led'],)
        )