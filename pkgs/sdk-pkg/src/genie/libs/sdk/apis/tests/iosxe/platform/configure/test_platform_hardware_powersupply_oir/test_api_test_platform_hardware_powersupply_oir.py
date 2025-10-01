from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import test_platform_hardware_powersupply_oir
from unittest.mock import Mock


class TestTestPlatformHardwarePowersupplyOir(TestCase):

    def test_test_platform_hardware_powersupply_oir(self):
        self.device = Mock()
        results_map = {
            'test platform hardware chassis power-supply 1 oir insert': 'Power-supply 1 is already inserted',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = test_platform_hardware_powersupply_oir(self.device, 1, 'insert')
        self.assertIn(
            'test platform hardware chassis power-supply 1 oir insert',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
