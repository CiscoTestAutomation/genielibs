from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.get import show_tech_support_platform_monitor
from unittest.mock import Mock


class TestShowTechSupportPlatformMonitor(TestCase):

    def test_show_tech_support_platform_monitor(self):
        self.device = Mock()
        results_map = {
            'show tech-support platform monitor 10 | redirect bootflash:show_tech_support_monitor': '',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = show_tech_support_platform_monitor(self.device, 'show_tech_support_monitor', 10)
        self.assertIn(
            'show tech-support platform monitor 10 | redirect bootflash:show_tech_support_monitor',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
