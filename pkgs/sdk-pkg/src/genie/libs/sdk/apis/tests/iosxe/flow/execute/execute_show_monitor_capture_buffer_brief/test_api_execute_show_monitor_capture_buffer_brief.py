from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.execute import execute_show_monitor_capture_buffer_brief
from unittest.mock import Mock


class TestExecuteShowMonitorCaptureBufferBrief(TestCase):

    def test_execute_show_monitor_capture_buffer_brief(self):
        self.device = Mock()
        results_map = {
            'show monitor capture t1 buffer brief': 'Starting the packet display ........ Press Ctrl + Shift + 6 to exit',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_monitor_capture_buffer_brief(self.device, 't1')
        self.assertIn(
            'show monitor capture t1 buffer brief',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = 'Starting the packet display ........ Press Ctrl + Shift + 6 to exit'
        self.assertEqual(result, expected_output)
