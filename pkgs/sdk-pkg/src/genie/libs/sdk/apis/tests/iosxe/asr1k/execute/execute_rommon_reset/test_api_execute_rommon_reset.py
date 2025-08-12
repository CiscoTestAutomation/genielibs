from unittest import TestCase
from genie.libs.sdk.apis.iosxe.asr1k.execute import execute_rommon_reset
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

System integrity status: 90170400 12030116

U

System Bootstrap, Version 16.9(4r), RELEASE SOFTWARE
Copyright (c) 1994-2018  by cisco Systems, Inc.


Current image running: Boot ROM1

Last reset cause: LocalSoft


ASR1002-HX platform with 16777216 Kbytes of main memory''',
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
