from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.execute import execute_monitor_capture_access_list
from unittest.mock import Mock


class TestExecuteMonitorCaptureAccessList(TestCase):

    def test_execute_monitor_capture_access_list(self):
        self.device = Mock()
        results_map = {
            'monitor capture C3 interface HundredGigE1/0/1 in access-list acl_1': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_monitor_capture_access_list(self.device, 'C3', 'acl_1', 'HundredGigE1/0/1', 'in', '')
        self.assertIn(
            'monitor capture C3 interface HundredGigE1/0/1 in access-list acl_1',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
