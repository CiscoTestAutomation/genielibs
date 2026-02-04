from unittest import TestCase
from genie.libs.sdk.apis.iosxe.isr4k.execute import execute_rommon_reset
from unittest.mock import Mock


class TestExecuteRommonReset(TestCase):

    def test_execute_rommon_reset(self):
        self.device = Mock()
        self.device.state_machine = Mock()
        self.device.state_machine.current_state = 'rommon'
        results_map = {
            'reset': '''
            Resetting .......
            Initializing Hardware ...
            Checking for PCIe device presence...done
            System integrity status: 0x610
            Rom image verified correctly
            System Bootstrap, Version 16.12(2r), RELEASE SOFTWARE
            Copyright (c) 1994-2019  by cisco Systems, Inc.
            Current image running: Boot ROM1
            Last reset cause: LocalSoft
            ISR4351/K9 platform with 4194304 Kbytes of main memory''',
        }

        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)

        self.device.execute.side_effect = results_side_effect

        result = execute_rommon_reset(self.device, 300)
        self.assertIn(
            'reset',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
