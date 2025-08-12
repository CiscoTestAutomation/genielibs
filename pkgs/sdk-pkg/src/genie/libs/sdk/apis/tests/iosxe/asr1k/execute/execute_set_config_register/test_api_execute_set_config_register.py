import os
from pyats.topology import loader
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.asr1k.execute import execute_set_config_register

class TestExecuteSetConfigRegister(TestCase):

    def test_execute_set_config_register(self):
        self.device = Mock()
        self.device.default = Mock()
        self.device.default.state_machine = Mock()
        self.device.default.state_machine.current_state = 'rommon'
        self.device.subconnections = [self.device.default]
        results_map = {
            'confreg 0x0': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_set_config_register(self.device,'0x0', 300)

        self.assertIn(
            'confreg 0x0',
            self.device.default.execute.call_args_list[0][0]
        )
        expected_cmd = f'confreg 0x0'
        expected_output = None
        self.assertEqual(result, expected_output)


