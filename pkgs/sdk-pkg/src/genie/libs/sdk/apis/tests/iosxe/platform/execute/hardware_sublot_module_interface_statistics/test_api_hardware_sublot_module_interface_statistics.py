from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import hardware_sublot_module_interface_statistics
from unittest.mock import Mock


class TestHardwareSublotModuleInterfaceStatistics(TestCase):

    def test_hardware_sublot_module_interface_statistics(self):
        self.device = Mock()
        results_map = {
            'show platform hardware subslot 0/0 module interface GigabitEthernet0/0/0 statistics':
            '''GigabitEthernet 0/0/0 Cumulative Statistics:
            
            Input packet count             9215
            Input bytes count              42713459
            Input mcast packets            0
            Input bcast packets            9
            Input CRC errors               0
            Input overruns                 0
            Runt packets                   0
            Giant packets                  0
            Input pause frames             0
            Output packet count            9216
            Output bytes count             42713527
            Output mcast packets           0
            Output bcast packets           12
            Output underruns               0
            Output pause frames            0''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = hardware_sublot_module_interface_statistics(self.device, '0/0', 'GigabitEthernet0/0/0')
        self.assertIn(
            'show platform hardware subslot 0/0 module interface GigabitEthernet0/0/0 statistics',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
