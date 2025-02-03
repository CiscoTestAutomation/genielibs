from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import set_platform_software_ilpower_mcu
from unittest.mock import Mock


class TestSetPlatformSoftwareIlpowerMcu(TestCase):

    def test_set_platform_software_ilpower_mcu(self):
        self.device = Mock()
        results_map = {
            'set platform software ilpower switch active R0 MCU enable': 'MCU console logging is already enabled',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = set_platform_software_ilpower_mcu(self.device, 'active', 'R0', 'enable')
        self.assertIn(
            'set platform software ilpower switch active R0 MCU enable',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
