from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_factory_reset
from unittest.mock import Mock


class TestExecuteFactoryReset(TestCase):

    def test_execute_factory_reset(self):
        self.device = Mock()
        results_map = {
            'factory-reset all secure': 'Enter interface name used to connect to the'
'management network from the above interface summary:IP address for this interface:',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_factory_reset(self.device, True, True, False, None, None, None, False, False, 60, 1200, 'emgy0', 'ie9k_iosxe.BLD_POLARIS_DEV_LATEST_20240919_003342.SSA.bin', 'Cisco123&*', None, 'Cisco123&*', 'Cisco123&*', 'Vlan1', '192.168.1.1', '255.255.255.0')
        self.assertIn(
            'factory-reset all secure',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
