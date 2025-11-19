from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ethernet.execute import execute_show_ethernet_cfm_errors
from unittest.mock import Mock


class TestExecuteShowEthernetCfmErrors(TestCase):

    def test_execute_show_ethernet_cfm_errors(self):
        self.device = Mock()
        results_map = {
            'show ethernet cfm errors': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_ethernet_cfm_errors(self.device)
        self.assertIn(
            'show ethernet cfm errors',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
