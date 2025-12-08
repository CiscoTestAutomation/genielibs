from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_platform_hardware_sensor_value_cm
from unittest.mock import Mock


class TestExecuteTestPlatformHardwareSensorValueCm(TestCase):

    def test_execute_test_platform_hardware_sensor_value_cm(self):
        self.device = Mock()
        results_map = {
            'test platform hardware slot R1 sensor 148 cm-override off': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_test_platform_hardware_sensor_value_cm(self.device, 'R1', 148, None)
        self.assertIn(
            'test platform hardware slot R1 sensor 148 cm-override off',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
