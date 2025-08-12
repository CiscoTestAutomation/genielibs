from unittest import TestCase
from genie.libs.sdk.apis.iosxe.isr4k.execute import execute_set_config_register
from unittest.mock import Mock


class TestExecuteSetConfigRegister(TestCase):

    def test_execute_set_config_register(self):
        self.device = Mock()
        self.device.default = Mock()
        self.device.state_machine = Mock()
        self.device.state_machine.current_state = 'rommon'
        results_map = {
            'confreg 0x0': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_set_config_register(self.device,'0x0', 300)

        self.assertIn(
            'confreg 0x0',
            self.device.execute.call_args_list[0][0]
        )
        expected_cmd = f'confreg 0x0'
        expected_output = None
        self.assertEqual(result, expected_output)
