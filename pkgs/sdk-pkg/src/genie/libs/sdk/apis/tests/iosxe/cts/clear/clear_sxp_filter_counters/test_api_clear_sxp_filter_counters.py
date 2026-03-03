from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.clear import clear_sxp_filter_counters
from unittest.mock import Mock


class TestClearSxpFilterCounters(TestCase):

    def test_clear_sxp_filter_counters(self):
        self.device = Mock()
        results_map = {
            'clear cts sxp filter-counters': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_sxp_filter_counters(self.device)
        self.assertIn(
            'clear cts sxp filter-counters',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
