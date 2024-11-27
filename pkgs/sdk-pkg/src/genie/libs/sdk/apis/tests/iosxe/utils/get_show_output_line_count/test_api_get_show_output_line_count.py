import os
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.utils import get_show_output_line_count
from unittest.mock import Mock
class TestGetShowOutputLineCount(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_get_show_output_line_count(self):
        results_map = {
            'show version | count ott-c9300-46': 'Number of lines which match regexp = 1',
        }
        
        def results_side_effect(arg):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = get_show_output_line_count(self.device, 'show version', 'ott-c9300-46', None)
        self.assertIn(
            'show version | count ott-c9300-46',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = 1
        self.assertEqual(result, expected_output)
