from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flow.configure import clear_stealthwatch_cloud_data
from unittest.mock import Mock


class TestClearStealthwatchCloudData(TestCase):

    def test_clear_stealthwatch_cloud_data(self):
        self.device = Mock()
        results_map = {
            'clear platform software fed switch standby swc data': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_stealthwatch_cloud_data(self.device, 'standby')
        self.assertIn(
            'clear platform software fed switch standby swc data',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
