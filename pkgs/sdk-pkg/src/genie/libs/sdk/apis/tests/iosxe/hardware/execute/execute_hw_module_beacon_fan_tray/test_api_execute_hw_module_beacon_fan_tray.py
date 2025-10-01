from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.execute import execute_hw_module_beacon_fan_tray
from unittest.mock import Mock


class TestExecuteHwModuleBeaconFanTray(TestCase):

    def test_execute_hw_module_beacon_fan_tray(self):
        self.device = Mock()
        results_map = {
            'hw-module beacon switch 1 fan-tray 1 off': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_hw_module_beacon_fan_tray(self.device, 1, 'off', 1)
        self.assertIn(
            'hw-module beacon switch 1 fan-tray 1 off',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
