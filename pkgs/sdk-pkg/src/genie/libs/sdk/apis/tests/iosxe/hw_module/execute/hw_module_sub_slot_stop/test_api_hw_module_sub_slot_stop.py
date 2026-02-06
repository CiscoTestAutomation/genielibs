from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hw_module.execute import hw_module_sub_slot_stop
from unittest.mock import Mock


class TestHwModuleSubSlotStop(TestCase):

    def test_hw_module_sub_slot_stop(self):
        self.device = Mock()
        results_map = {
            'hw-module subslot 0/1 stop': 'Proceed with stop of module? [confirm]',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = hw_module_sub_slot_stop(self.device, '0/1')
        self.assertIn(
            'hw-module subslot 0/1 stop',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
