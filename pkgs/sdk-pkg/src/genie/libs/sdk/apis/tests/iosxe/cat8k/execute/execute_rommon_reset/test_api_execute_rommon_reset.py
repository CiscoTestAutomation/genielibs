from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cat8k.execute import execute_rommon_reset
from unittest.mock import Mock


class TestExecuteRommonReset(TestCase):

    def test_execute_rommon_reset(self):
        self.device = Mock()
        self.device.default = Mock()
        self.device.default.state_machine = Mock()
        self.device.default.state_machine.current_state = 'rommon'
        self.device.subconnections = [self.device.default]
        results_map = {
            'reset': '''


Resetting .......




Initializing Hardware ...


System integrity status: 90170200  14030117  00000300
Procyon RSM done


System Bootstrap, Version 17.11(1r), RELEASE SOFTWARE
Copyright (c) 1994-2023 by cisco Systems, Inc.

Current image running: Boot ROM1
Last reset cause: LocalSoft

C8500-12X4QC platform with 16777216 Kbytes of main memory
''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_rommon_reset(self.device)

        self.assertIn(
            'reset',
            self.device.default.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
