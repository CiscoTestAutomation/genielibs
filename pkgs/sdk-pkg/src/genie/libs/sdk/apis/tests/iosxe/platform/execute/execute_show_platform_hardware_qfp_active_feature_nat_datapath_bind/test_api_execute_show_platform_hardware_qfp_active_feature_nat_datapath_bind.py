from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_show_platform_hardware_qfp_active_feature_nat_datapath_bind
from unittest.mock import Mock


class TestExecuteShowPlatformHardwareQfpActiveFeatureNatDatapathBind(TestCase):

    def test_execute_show_platform_hardware_qfp_active_feature_nat_datapath_bind(self):
        self.device = Mock()
        results_map = {
            'show platform hardware qfp active feature nat datapath bind': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_show_platform_hardware_qfp_active_feature_nat_datapath_bind(self.device)
        self.assertIn(
            'show platform hardware qfp active feature nat datapath bind',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = ''
        self.assertEqual(result, expected_output)
