from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_locate_switch
from unittest.mock import Mock


class TestExecuteLocateSwitch(TestCase):

    def test_execute_locate_switch(self):
        self.device = Mock()
        results_map = {
            'locate-switch 10': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_locate_switch(self.device, 10, None, None)
        self.assertIn(
            'locate-switch 10',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
