from unittest import TestCase
from genie.libs.sdk.apis.iosxe.nat.execute import execute_clear_ip_nat_statistics
from unittest.mock import Mock


class TestExecuteClearIpNatStatistics(TestCase):

    def test_execute_clear_ip_nat_statistics(self):
        self.device = Mock()
        results_map = {
            'clear ip nat statistics': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_clear_ip_nat_statistics(self.device)
        self.assertIn(
            'clear ip nat statistics',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
