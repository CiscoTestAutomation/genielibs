from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import clear_counters
from unittest.mock import Mock

class TestClearCounters(TestCase):

    def test_clear_counters(self):
        self.device = Mock()
        results_map = {
            'clear counters': 'Clear "show interface" counters on all interfaces [confirm]',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_counters(self.device)
        self.assertIn(
            'clear counters',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
