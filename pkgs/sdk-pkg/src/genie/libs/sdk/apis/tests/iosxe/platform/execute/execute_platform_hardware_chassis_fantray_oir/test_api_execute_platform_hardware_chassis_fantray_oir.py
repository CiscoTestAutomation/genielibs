from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_platform_hardware_chassis_fantray_oir
from unittest.mock import Mock


class TestExecutePlatformHardwareChassisFantrayOir(TestCase):

    def test_execute_platform_hardware_chassis_fantray_oir(self):
        self.device = Mock()
        results_map = {
            'test platform hardware chassis fantray 1 oir insert': 'Fantray 1 is already inserted',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_platform_hardware_chassis_fantray_oir(self.device, '1', 'insert', 60)
        self.assertIn(
            'test platform hardware chassis fantray 1 oir insert',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
