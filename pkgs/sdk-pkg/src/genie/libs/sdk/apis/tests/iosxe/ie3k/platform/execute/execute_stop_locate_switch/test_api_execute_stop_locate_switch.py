from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_stop_locate_switch
from unittest.mock import Mock


class TestExecuteStopLocateSwitch(TestCase):

    def test_execute_stop_locate_switch(self):
        self.device = Mock()
        results_map = {
            'locate-switch switch active 0': 'Locate Switch disabled!!',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_stop_locate_switch(self.device, None, 'active')
        self.assertIn(
            'locate-switch switch active 0',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
