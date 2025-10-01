from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import clear_cts_environment_data
from unittest.mock import Mock


class TestClearCtsEnvironmentData(TestCase):

    def test_clear_cts_environment_data(self):
        self.device = Mock()
        results_map = {
            'clear cts environment-data': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = clear_cts_environment_data(self.device)
        self.assertIn(
            'clear cts environment-data',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
