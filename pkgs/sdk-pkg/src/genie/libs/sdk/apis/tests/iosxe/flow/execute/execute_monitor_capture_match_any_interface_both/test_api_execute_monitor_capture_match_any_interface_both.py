from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.execute import execute_monitor_capture_match_any_interface_both
from unittest.mock import Mock


class TestExecuteMonitorCaptureMatchAnyInterfaceBoth(TestCase):

    def test_execute_monitor_capture_match_any_interface_both(self):
        self.device = Mock()
        results_map = {
            'monitor capture t1 match any interface TenGigabitEthernet1/0/15 both': 'A filter is already attached to the capture. Replace with specified filter?[confirm]',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_monitor_capture_match_any_interface_both(self.device, 't1', 'TenGigabitEthernet1/0/15')
        self.assertIn(
            'monitor capture t1 match any interface TenGigabitEthernet1/0/15 both',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
