from unittest import TestCase
from genie.libs.sdk.apis.iosxe.apphosting.configure import count_trace_in_logging
from unittest.mock import Mock


class TestCountTraceInLogging(TestCase):

    def test_count_trace_in_logging(self):
        self.device = Mock()
        results_map = {
            'sh logging | count Trace': 'Number of lines which match regexp = 0',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = count_trace_in_logging(self.device)
        self.assertIn(
            'sh logging | count Trace',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
