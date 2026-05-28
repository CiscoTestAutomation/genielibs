from unittest import TestCase
from genie.libs.sdk.apis.iosxe.pki.execute import execute_show_monitor_event_trace
from unittest.mock import Mock


class TestExecuteShowMonitorEventTrace(TestCase):

    def test_execute_show_monitor_event_trace(self):
        self.device = Mock()
        results_map = {
            'show monitor event-trace redundancy latest': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_monitor_event_trace(self.device, 'redundancy latest')
        self.assertIn(
            'show monitor event-trace redundancy latest',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
