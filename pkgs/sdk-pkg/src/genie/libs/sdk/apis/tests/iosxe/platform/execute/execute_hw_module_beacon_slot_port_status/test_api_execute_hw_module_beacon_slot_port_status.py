from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_hw_module_beacon_slot_port_status
from unittest.mock import Mock


class TestExecuteHwModuleBeaconSlotPortStatus(TestCase):

    def test_execute_hw_module_beacon_slot_port_status(self):
        self.device = Mock()
        results_map = {
            'hw-module beacon slot 1 port 1 status': 'BEACON OFF',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_hw_module_beacon_slot_port_status(self.device, '1', '1', 'status', 60)
        self.assertIn(
            'hw-module beacon slot 1 port 1 status',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = 'BEACON OFF'
        self.assertEqual(result, expected_output)
