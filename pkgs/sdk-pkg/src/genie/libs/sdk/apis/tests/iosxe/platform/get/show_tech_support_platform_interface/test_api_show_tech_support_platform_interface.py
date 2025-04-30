from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.get import show_tech_support_platform_interface
from unittest.mock import Mock


class TestShowTechSupportPlatformInterface(TestCase):

    def test_show_tech_support_platform_interface(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform interface HundredGigE2/0/17 | redirect bootflash:show_tech_support_interface_FiftyGigE1_0_16': None,
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_platform_interface(self.device, 'show_tech_support_interface_FiftyGigE1_0_16', 'HundredGigE2/0/17', None)
        self.assertIn(
            'show tech-support platform interface HundredGigE2/0/17 | redirect bootflash:show_tech_support_interface_FiftyGigE1_0_16',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
