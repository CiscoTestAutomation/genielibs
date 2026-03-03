from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hsr.configure import configure_fpga_profile
from unittest.mock import Mock


class TestConfigureFpgaProfile(TestCase):

    def test_configure_fpga_profile(self):
        self.device = Mock()
        results_map = {
            'fpga-profile activate hsr-quadbox': '% FPGA profile  : hsr-quadbox is already activated',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = configure_fpga_profile(self.device, 'hsr-quadbox')
        self.assertIn(
            'fpga-profile activate hsr-quadbox',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
