from unittest import TestCase
from genie.libs.sdk.apis.iosxe.zone.execute import execute_clear_zone_pair
from unittest.mock import Mock


class TestExecuteClearZonePair(TestCase):

    def test_execute_clear_zone_pair(self):
        self.device = Mock()
        results_map = {
            'clear zone-pair counter': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_clear_zone_pair(self.device, 'counter')
        self.assertIn(
            'clear zone-pair counter',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
