from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_test_platform_hardware_led_switch
from unittest.mock import Mock


class TestExecuteTestPlatformHardwareLedSwitch(TestCase):

    def test_execute_test_platform_hardware_led_switch(self):
        self.device = Mock()
        results_map = {
            'test platform hardware led switch active 1 1': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_platform_hardware_led_switch(self.device, 'active', 1, 1)
        self.assertIn(
            'test platform hardware led switch active 1 1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
