from unittest import TestCase
from genie.libs.sdk.apis.iosxe.debug.configure import debug_software_cpm_switch_feature
from unittest.mock import Mock


class TestDebugSoftwareCpmSwitchFeature(TestCase):

    def test_debug_software_cpm_switch_feature(self):
        self.device = Mock()
        results_map = {
            'debug platform software cpm switch 2 bp active link_preference disable': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = debug_software_cpm_switch_feature(self.device, '2', 'link_preference', 'disable', True)
        self.assertIn(
            'debug platform software cpm switch 2 bp active link_preference disable',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
