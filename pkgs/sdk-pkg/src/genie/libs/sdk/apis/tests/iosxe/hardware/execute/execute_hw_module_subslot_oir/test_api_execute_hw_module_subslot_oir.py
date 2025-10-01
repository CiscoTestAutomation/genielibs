from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.execute import execute_hw_module_subslot_oir
from unittest.mock import Mock


class TestExecuteHwModuleSubslotOir(TestCase):

    def test_execute_hw_module_subslot_oir(self):
        self.device = Mock()
        results_map = {
            'hw-module switch 1 subslot 1/0 oir insert': 'Proceed with insertion of module? [confirm]',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_hw_module_subslot_oir(self.device, 1, 'insert', 1)
        self.assertIn(
            'hw-module switch 1 subslot 1/0 oir insert',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = 'Proceed with insertion of module? [confirm]'
        self.assertEqual(result, expected_output)
