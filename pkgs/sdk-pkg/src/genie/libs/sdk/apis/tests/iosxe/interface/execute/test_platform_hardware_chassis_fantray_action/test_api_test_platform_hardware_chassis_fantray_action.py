from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.execute import test_platform_hardware_chassis_fantray_action
from unittest.mock import Mock


class TestTestPlatformHardwareChassisFantrayAction(TestCase):

    def test_test_platform_hardware_chassis_fantray_action(self):
        self.device = Mock()
        results_map = {
            'test platform hardware chassis fantray 1 fan 1 inlet lock-speed': 'success',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = test_platform_hardware_chassis_fantray_action(self.device, 1, 1, 'inlet', 'lock-speed')
        self.assertIn(
            'test platform hardware chassis fantray 1 fan 1 inlet lock-speed',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
